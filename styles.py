# желтый цвет иконок - #ffea00
STYLE_LIGHT = """
    * {
        background: white;
    }
"""

STYLE_DARK = """
    QWidget#LauncherUI {
        background: #343434;
        color: white;
    }
    QWidget#AboutGameFrame {
        background: #343434;
        color: white;
    }
    QWidget#scroll_widget {
        background: #28282B;
        color: white;
    }
    QScrollArea#scroll_widget {
        background: #343434;
        color: white;
        border: 1px solid #28282B;
    }
    QWidget#FooterFrame {
        background: #28282B;
    }

    QPushButton#G-NewGame {
        background: #28282B;
        color: #ffea00;
        border-radius: 15%;
    }
    QPushButton#G-NewGame:hover {
        background: rgba(0, 173, 255, 0.2);
    }
    QPushButton#G-NewGame:pressed {
        background: rgba(0, 173, 255, 0.5);
    }

    QPushButton#AG-LaunchGame {
        background: #ffea00;
        color: #28282B;
        border-radius: 1%;
    }
    QPushButton#AG-LaunchGame:hover {
        background: rgba(239, 221, 16, 0.7);
    }
    QPushButton#AG-LaunchGame:pressed {
        background: rgba(239, 221, 16, 0.5);
    }

    QPushButton#AG-GameSettings {
        background: transparent;
        color: #28282B;
        border-radius: 25%;
    }
    QPushButton#AG-GameSettings:hover {
        background: rgba(0, 173, 255, 0.2);
    }
    QPushButton#AG-GameSettings:pressed {
        background: rgba(0, 173, 255, 0.5);
    }

    QMenu::item {
        color: black;
    }
    QMenu::item:selected {
        color: red;
    }

    QLabel#NB-Title {
        background: #28282B;
        color: #ffea00;
    }
    QWidget#NavBarFrame {
        background: #28282B;
        color: white;
    }
    QPushButton#NB-Buttuns {
        background: #28282B;
        color: red;
        border-radius: 10%;
    }
    QPushButton#NB-Buttuns:hover {
        background: rgba(0, 173, 255, 0.2);
    }
    QPushButton#NB-Buttuns:pressed {
        background: rgba(0, 173, 255, 0.5);
    }

    QWidget#GeneralAreaFrame {
        background: #343434;
        color: white;
    }

    QWidget#GeneralAreaFrame2 {
        background: #343434;
        border: 1px solid #28282B;
    }
    QLabel#AS-OptionLabel {
        color: white;
    }

    QComboBox {
        background: transparent;
        color: white;
        /*border: 1px solid #28282B;*/
    }
    QComboBox:drop-down {
        width: 0px;
        height: 0px;
        border: 0px;
    }
    QComboBox QAbstractItemView {
        color: white;	
        background: #343434;
        padding: 5px;
    }
    QComboBox QScrollBar {
        width: 0px;
        height: 0px;
        border: 0px;
    }
    QComboBox:hover {
        background: rgba(0, 173, 255, 0.2);
        border-radius: 1%;
    }

    QPushButton#AS-ToggleBtn {
        background: transparent;
        border-radius: 10%;
    }
    QPushButton#AS-ToggleBtn:hover {
        background: rgba(0, 173, 255, 0.2);
    }
    QPushButton#AS-ToggleBtn:pressed {
        background: rgba(0, 173, 255, 0.5);
    }

    QPushButton#AS-ImportExportBtn {
        background: transparent;
        color: white;
        border-radius: 10%;
    }
    QPushButton#AS-ImportExportBtn:hover {
        background: rgba(0, 173, 255, 0.2);
    }
    QPushButton#AS-ImportExportBtn:pressed {
        background: rgba(0, 173, 255, 0.5);
    }

    QLabel#GS-Labels {
        background: transparent;
        color: white;
    }
    
    QTextEdit#ted_game_title {
        background: transparent;
        color: white;
        border: 0px;
    }
    QTextEdit#ted_game_title:hover {
        background: rgba(211, 211, 211, 0.2);
    }

    QTextEdit#GS-TedPaths {
        background: transparent;
        color: #ffea00;
        border: 0px;
    }

    QPushButton#GS-EditButtons {
        background: transparent;
        border-radius: 10%;
    }
    QPushButton#GS-EditButtons:hover {
        background: rgba(0, 173, 255, 0.2);
    }
    QPushButton#GS-EditButtons:pressed {
        background: rgba(0, 173, 255, 0.5);
    }

    QPushButton#GS-ControlButtons {
        background: #ffea00;
        color: #28282B;
        border-radius: 10%;
    }
    QPushButton#GS-ControlButtons:hover {
        background: rgba(239, 221, 16, 0.7);
    }
    QPushButton#GS-ControlButtons:pressed {
        background: rgba(239, 221, 16, 0.5);
    }

    QWidget#GeneralAreaFrame3 {
        background: #343434;
        border: 1px solid #28282B;
    }
"""
