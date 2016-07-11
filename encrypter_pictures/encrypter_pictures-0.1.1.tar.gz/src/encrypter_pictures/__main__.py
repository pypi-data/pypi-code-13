from gui import QApplication, ImageViewer
import sys

def main(args=None):
    app = QApplication(sys.argv)
    imageViewer = ImageViewer()
    imageViewer.showMaximized()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
