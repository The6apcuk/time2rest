from PyQt5 import QtWidgets
from model import Request, Requests, Endpoint, Endpoints
from persistent_model import FileInt

from view_requests import ViewRequests
from view_endpoints import ViewEndpoints

import sys

# Init app
app = QtWidgets.QApplication(sys.argv)

# Init models
requests = Requests(FileInt('URI_DBS', str(Requests.name)))
eps = Endpoints(FileInt('URI_DBS', str(Endpoints.name)))

# Init windows
main_window = QtWidgets.QMainWindow()
dialog = QtWidgets.QDialog()

# Init Views
endpoint_view = ViewEndpoints(dialog, eps)
requests_view = ViewRequests(main_window, dialog, requests, eps)

# Show main window
main_window.show()

# Execute application
sys.exit(app.exec_())
