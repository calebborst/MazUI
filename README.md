# MazPi

MazPi is a custom web-based car display system designed for a Mazda 6 (2003) using a Raspberry Pi 4. Inspired by OpenAuto Pro, this project aims to provide a stylish and functional user interface for in-car information and entertainment.

## Features

- **Web-Based Interface**: Powered by Flask, accessible via a localhost web server.
- **Bluetooth Integration**: Connects seamlessly to a transmitter for audio and data.
- **Customizable UI**: Designed with a focus on clean and modern web design elements.
- **Auto-Opening Mechanism**: Includes motorized functionality for the display panel.
- **Real-Time Vehicle Data**: Fetches and displays OBD-II metrics using the `obd` library.
- **Media Support**: Handles music and other media playback with the `mutagen` library.

## Installation

1. **Clone the Repository**
   `git clone https://github.com/your-username/mazpi.git`
   `cd mazpi`

2. **Install Dependencies**
   Ensure you have Python 3.x installed. Then run:
   `pip install -r requirements.txt`

3. **Run the Application**
   `python app.py`

4. **Access the Web Interface**
   Open a browser and navigate to `http://localhost:5000`.

## Dependencies

This project requires the following Python libraries, as listed in `requirements.txt`:

```
blinker==1.9.0
click==8.1.7
colorama==0.4.6
Flask==3.1.0
itsdangerous==2.2.0
Jinja2==3.1.4
MarkupSafe==3.0.2
mutagen==1.47.0
obd==0.7.2
Pint==0.20.1
pyserial==3.5
Werkzeug==3.1.3
```

## Hardware Requirements

- Raspberry Pi 4
- Bluetooth transmitter
- Motorized screen hardware
- Mazda 6 (2003) compatible OBD-II reader

## Roadmap

- **Phase 1**: Complete the core web interface and vehicle data integration.
- **Phase 2**: Develop motorized display controls.
- **Phase 3**: Optimize for deployment on Linux for in-car use.
- **Phase 4**: Add media playback and additional car-specific features.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Inspired by [OpenAuto Pro](https://github.com/openDsh/openauto)
- Developed using Flask and Raspberry Pi hardware

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for bug fixes, enhancements, or new features.
