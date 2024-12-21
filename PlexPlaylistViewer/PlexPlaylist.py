from cryptography.fernet import Fernet
import os
import json
import tkinter as tk
from tkinter import Tk, simpledialog, messagebox, ttk, filedialog
from plexapi.server import PlexServer

# File paths for key and encrypted data
KEY_FILE = "key.key"
DATA_FILE = "data.enc"

def generate_key():
    """Generate a new encryption key and save it."""
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as key_file:
        key_file.write(key)
    return key

def load_key():
    """Load the encryption key from the file."""
    if not os.path.exists(KEY_FILE):
        return generate_key()
    with open(KEY_FILE, "rb") as key_file:
        return key_file.read()

def encrypt_data(data, key):
    """Encrypt data using the provided key."""
    fernet = Fernet(key)
    encrypted = fernet.encrypt(data.encode())
    with open(DATA_FILE, "wb") as data_file:
        data_file.write(encrypted)

def decrypt_data(key):
    """Decrypt data using the provided key."""
    if not os.path.exists(DATA_FILE):
        return None
    with open(DATA_FILE, "rb") as data_file:
        encrypted = data_file.read()
    fernet = Fernet(key)
    return fernet.decrypt(encrypted).decode()

def get_plex_credentials():
    """Prompt for Plex IP and Token if not already stored."""
    key = load_key()

    decrypted_data = decrypt_data(key)
    if decrypted_data:
        return json.loads(decrypted_data)

    root = Tk()
    root.withdraw()
    ip = simpledialog.askstring("Plex Server IP", "Enter Plex Server IP:")
    token = simpledialog.askstring("Plex Token", "Enter Plex Token:", show="*")

    if not ip or not token:
        messagebox.showerror("Error", "IP and Token are required.")
        raise ValueError("IP and Token are required.")

    data = json.dumps({"ip": ip, "token": token})
    encrypt_data(data, key)
    return {"ip": ip, "token": token}

class PlexPlaylistApp:
    def __init__(self, root, ip, token):
        self.root = root
        self.root.title("Plex Musical Playlist Viewer")
        self.root.geometry("600x400")  # Set initial size
        self.root.minsize(400, 300)  # Set minimum size

        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)

        self.baseurl = f"http://{ip}:32400"
        self.token = token
        self.plex = PlexServer(self.baseurl, self.token)
        self.music_playlists = []
        self.current_playlist_data = None  

        self.load_music_playlists()

    def load_music_playlists(self):
        playlists = self.plex.playlists()
        self.music_playlists = [playlist for playlist in playlists if playlist.playlistType == 'audio']

        if not self.music_playlists:
            messagebox.showinfo("No Playlists", "No music playlists found on the server.")
            return

        self.create_playlist_frame()

    def create_playlist_frame(self):
        self.frame = ttk.Frame(self.root, padding="10")
        self.frame.grid(row=0, column=0, sticky="nsew")

        self.frame.rowconfigure(2, weight=1)
        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=1)

        ttk.Label(self.frame, text="Select a Playlist:").grid(row=0, column=0, sticky="w", padx=5, pady=5)

        self.playlist_var = tk.StringVar()
        self.playlist_dropdown = ttk.Combobox(self.frame, textvariable=self.playlist_var, state="readonly")
        self.playlist_dropdown['values'] = [playlist.title for playlist in self.music_playlists]
        self.playlist_dropdown.grid(row=0, column=1, padx=5, pady=5)

        ttk.Button(self.frame, text="View Songs", command=self.display_songs).grid(row=1, column=0, columnspan=2, pady=10)

        self.text_window = tk.Text(self.frame, wrap="word", state="disabled")
        self.text_window.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

        # Add Export and Close buttons
        buttons_frame = ttk.Frame(self.frame)
        buttons_frame.grid(row=3, column=0, columnspan=2, pady=10, sticky="e")

        ttk.Button(buttons_frame, text="Export", command=self.export_playlist).grid(row=0, column=0, padx=5)
        ttk.Button(buttons_frame, text="Close", command=self.root.destroy).grid(row=0, column=1, padx=5)

    def display_songs(self):
        selected_title = self.playlist_var.get()
        if not selected_title:
            messagebox.showerror("Selection Error", "Please select a playlist from the dropdown.")
            return

        selected_playlist = next((playlist for playlist in self.music_playlists if playlist.title == selected_title), None)
        if not selected_playlist:
            messagebox.showerror("Playlist Error", "Unable to find the selected playlist.")
            return

        songs = selected_playlist.items()
        duration_seconds = selected_playlist.duration / 1000  # Convert milliseconds to seconds
        duration_minutes = round(duration_seconds / 60, 2)

        playlist_data = [f"Songs in Playlist: {selected_playlist.title} (Duration: {duration_minutes} minutes)\n"]
        for song in songs:
            artist = song.artist()
            artist_name = artist.title if artist else "Unknown Artist"

            album = song.album()
            album_name = album.title if album else "Unknown Album"

            playlist_data.append(f"- {song.title} by {artist_name} (Album: {album_name})")

        self.current_playlist_data = "\n".join(playlist_data)

        self.text_window.configure(state="normal")
        self.text_window.delete("1.0", "end")
        self.text_window.insert("end", self.current_playlist_data)
        self.text_window.configure(state="disabled")

    def export_playlist(self):
        if not self.current_playlist_data:
            messagebox.showerror("Export Error", "No playlist data to export. Please view a playlist first.")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
            title="Save Playlist"
        )
        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write(self.current_playlist_data)
                messagebox.showinfo("Export Successful", f"Playlist saved to {file_path}")
            except Exception as e:
                messagebox.showerror("Export Error", f"Failed to save the playlist: {e}")

# Main Application
if __name__ == "__main__":
    try:
        credentials = get_plex_credentials()
        root = Tk()
        app = PlexPlaylistApp(root, credentials['ip'], credentials['token'])
        root.mainloop()
    except Exception as e:
        print(f"Error: {e}")
