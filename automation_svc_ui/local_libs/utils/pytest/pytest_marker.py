def get_pytest_marker(request, marker_name):
    for mark in request.node.own_markers:
        if mark.name == marker_name:
            marker_name = True
            return marker_name
