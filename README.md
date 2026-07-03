# SensDash
In its current state, this program uses python to simulate a cars dashboard. The data is generated randomly in the backend while the frontend uses PySide6 to generate the GUI. Eventually the GUI will pull realtime data from an arduino, and the project will evolve from there.

Start Up Requirements:
- Ensure that your IDE or Computer has the correct python installed (I'm currently using Python 3.14.0)
- Next create a virtual environment within the "Dashboard Frontend" folder using this command:
                   python -m venv venv (Windows)
                   python3 -m venv .venv (Macintosh)
- Then start the virtual environment using this command:
                   .\venv\Scripts\Activate.ps1 (Powershell)
                   source .venv/bin/activate (Macintosh)
- Then you will need to download the proper libraries
                    pip install PySide6
                    python -m pip install qtawesome
                    python3 -m pip install qtawesome (if you are using Mac)
