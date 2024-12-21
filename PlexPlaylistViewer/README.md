# Plex Playlist Viewer
> Script that launches a UI to view music playlist from your Plex server and allows export to txt file for sharing.


Query your server to pull a list of all your music playlists. Export playlists to txt file for easy sharing. Stores server IP and Plex user token in encrypted files so you dont have to keep entering them.

![Screenshot from 2024-12-20 20-20-04](https://github.com/user-attachments/assets/ae3ffadf-fe39-467b-bd58-6040ee90b6e7)


## Installation

Linux:

```sh
pip install -r requirements.txt
```

Windows:

```sh
pip install -r requirements.txt
```


## Usage
On first run, you will be prompted to enter the IP and user token for your Plex Server.

![Screenshot from 2024-12-20 20-26-25](https://github.com/user-attachments/assets/91c29cea-c091-4973-a935-a4918ed12c9a)

![Screenshot from 2024-12-20 20-26-38](https://github.com/user-attachments/assets/261d676c-ce47-4fb8-bd60-c1ab15d441cf)

![Screenshot from 2024-12-20 20-27-01](https://github.com/user-attachments/assets/fe559635-7a1d-4caf-be27-92d6fe94e6fd)

Once the interface loads, close and reopen. As long as the key.key and data.enc exist, you won't be asked for this information in the future. Should the files be deleted, you will have to re-enter the information before using the application.

Once loaded, select a playlist from the dropdown and click View Songs. This will display the playlist name and playlist duration along with song, artist and album. The UI is dynamic so it can be resized. If you want to share the playlist, click the export button to save the playlist as a txt file.


![Screenshot from 2024-12-20 20-36-03](https://github.com/user-attachments/assets/bfc1472e-85f9-4941-ab5e-7784fd9ffd34)




## Release History

* 0.0.1
    * Work in progress





