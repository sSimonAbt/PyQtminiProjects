class QObject():
    def __init__(self):
        self.name = "label"

class QWidget(QObject):
    def __init__(self):
        super().__init__()
        self.geometry = []
        self.font = "Arial"

class QFrame(QWidget):
    pass

class QLabel(QFrame):
    def __init__(self):
        super().__init__()
        self.text = "Hallo Welt"