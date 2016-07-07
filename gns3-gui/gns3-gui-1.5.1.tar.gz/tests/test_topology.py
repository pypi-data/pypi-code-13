# -*- coding: utf-8 -*-
#
# Copyright (C) 2015 GNS3 Technologies Inc.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import uuid
import os
from unittest.mock import patch, MagicMock

from gns3.topology import Topology
from gns3.project import Project
from gns3.version import __version__
from gns3.items.pixmap_image_item import PixmapImageItem
import gns3.main_window
import gns3.qt


def test_topology_init():
    Topology()


def test_topology_node(vpcs_device):
    topology = Topology()
    topology.addNode(vpcs_device)
    assert len(topology.nodes()) == 1
    assert topology.getNode(vpcs_device.id()) == vpcs_device
    topology.removeNode(vpcs_device)
    assert len(topology.nodes()) == 0


def test_dump(vpcs_device, project, local_server):
    topology = Topology()
    topology.project = project
    topology.addNode(vpcs_device)

    dump = topology.dump(include_gui_data=False)
    assert dict(dump) == {
        "project_id": project.id(),
        "auto_start": False,
        "name": project.name(),
        "version": __version__,
        "revision": 4,
        "topology": {
            "nodes": [
                {
                    "description": "VPCS device",
                    "id": vpcs_device.id(),
                    "ports": [
                        {
                            "id": vpcs_device.ports()[0].id(),
                            "name": "Ethernet0",
                            "port_number": 0,
                            "adapter_number": 0
                        }
                    ],
                    "properties": {
                        "name": vpcs_device.name()
                    },
                    "server_id": local_server.id(),
                    "type": "VPCSDevice",
                    "vm_id": None
                }
            ],
            "servers": [
                {
                    "vm": False,
                    "host": "127.0.0.1",
                    "id": local_server.id(),
                    "local": True,
                    "port": 3080,
                    "protocol": "http",
                }
            ]
        },
        "type": "topology"
    }


def test_dump_http_auth(vpcs_device, project, remote_server):

    remote_server.setUser("hello")
    remote_server.setPassword("world")

    from gns3.modules.vpcs.vpcs_device import VPCSDevice
    from gns3.modules.vpcs import VPCS

    vpcs_device = VPCSDevice(VPCS(), remote_server, project)
    vpcs_device._vpcs_device_id = str(uuid.uuid4())
    vpcs_device._settings = {"name": "VPCS 1", "script_file": "", "console": None, "startup_script": None}
    vpcs_device.setInitialized(True)

    topology = Topology()
    topology.project = project
    topology.addNode(vpcs_device)

    dump = topology.dump(include_gui_data=False)
    assert dict(dump) == {
        "project_id": project.id(),
        "auto_start": False,
        "name": project.name(),
        "version": __version__,
        "revision": 4,
        "topology": {
            "nodes": [
                {
                    "description": "VPCS device",
                    "id": vpcs_device.id(),
                    "ports": [
                        {
                            "id": vpcs_device.ports()[0].id(),
                            "name": "Ethernet0",
                            "port_number": 0,
                            "adapter_number": 0
                        }
                    ],
                    "properties": {
                        "name": vpcs_device.name()
                    },
                    "server_id": remote_server.id(),
                    "type": "VPCSDevice",
                    "vm_id": None
                }
            ],
            "servers": [
                {
                    "vm": False,
                    "host": "127.0.0.1",
                    "id": remote_server.id(),
                    "local": False,
                    "port": 8001,
                    "protocol": "http",
                    "user": "hello"
                }
            ]
        },
        "type": "topology"
    }


def test_randomize_id(project, tmpdir):
    project.setTopologyFile(str(tmpdir / "test.gns3"))

    project_uuid = str(uuid.uuid4())
    vm_uuid1 = str(uuid.uuid4())
    os.makedirs(str(tmpdir / "project-files" / "vpcs" / vm_uuid1))
    open(str(tmpdir / "project-files" / "vpcs" / vm_uuid1 / "test.log"), "w+").close()
    vm_uuid2 = str(uuid.uuid4())
    orig_topology = {
        "project_id": project_uuid,
        "topology": {
            "nodes": [
                {
                    "vm_id": vm_uuid1,
                },
                {
                    "vm_id": vm_uuid2
                }
            ]
        }
    }
    topology = Topology()
    topology.project = project
    top = topology._randomize_id(orig_topology)
    assert top["project_id"] != project_uuid
    assert top["topology"]["nodes"][0]["vm_id"] != vm_uuid1

    assert not os.path.exists(str(tmpdir / "project-files" / "vpcs" / vm_uuid1 / "test.log"))
    assert os.path.exists(str(tmpdir / "project-files" / "vpcs" / top["topology"]["nodes"][0]["vm_id"] / "test.log"))

    assert top["topology"]["nodes"][1]["vm_id"] != vm_uuid2
    assert top["topology"]["nodes"][0]["vm_id"] != top["topology"]["nodes"][1]["vm_id"]


def test_dump_random_id(vpcs_device, project, local_server):
    topology = Topology()
    topology.project = project
    topology.addNode(vpcs_device)

    fake_uuid = str(uuid.uuid4())
    with patch("uuid.uuid4", return_value=fake_uuid):
        dump = topology.dump(include_gui_data=False, random_id=True)
        assert dict(dump) == {
            "project_id": fake_uuid,
            "auto_start": False,
            "name": project.name(),
            "version": __version__,
            "revision": 4,
            "topology": {
                "nodes": [
                    {
                        "id": vpcs_device.id(),
                        "description": "VPCS device",
                        "ports": [
                            {
                                "id": vpcs_device.ports()[0].id(),
                                "name": "Ethernet0",
                                "port_number": 0,
                                "adapter_number": 0
                            }
                        ],
                        "properties": {
                            "name": vpcs_device.name()
                        },
                        "server_id": local_server.id(),
                        "type": "VPCSDevice",
                        "vm_id": fake_uuid}
                ],
                "servers": [
                    {
                        "host": "127.0.0.1",
                        "id": local_server.id(),
                        "local": True,
                        "port": 3080,
                        "protocol": "http",
                        "vm": False
                    }
                ]
            },
            "type": "topology"
        }


def test_loadFile(tmpdir):
    topology = Topology()
    topo = str(tmpdir / "test" / "test.gns3")

    os.makedirs(str(tmpdir / "test"))
    with open(topo, 'w+') as f:
        f.write('{"name": "test", "type": "topology", "auto_start": false, "project_id": null, "topology": {}}')

    with patch("gns3.topology.Topology._load") as mock:
        project = Project()
        topology.loadFile(topo, project)

        assert mock.called
        args, kwargs = mock.call_args
        assert args[0] == {"name": "test", "auto_start": False, "project_id": None, "topology": {}, "type": "topology"}
        assert topology._project.filesDir() == str(tmpdir / "test")
        assert topology._project.name() == "test"


def test_load(project, monkeypatch, main_window, tmpdir):

    topo = {
        "project_id": project.id(),
        "auto_start": False,
        "name": "twovpcs",
        "topology": {
            "links": [
                {
                    "description": "Link from VPCS 1 port Ethernet0 to VPCS 2 port Ethernet0",
                    "destination_node_id": 2,
                    "destination_port_id": 2,
                    "id": 1,
                    "source_node_id": 1,
                    "source_port_id": 1
                }
            ],
            "nodes": [
                {
                    "description": "VPCS device",
                    "id": 1,
                    "label": {
                        "color": "#000000",
                        "font": "TypeWriter,10,-1,5,75,0,0,0,0,0",
                        "text": "VPCS 1",
                        "x": 10.75,
                        "y": -25.0
                    },
                    "ports": [
                        {
                            "description": "connected to VPCS 2 on port Ethernet0",
                            "id": 1,
                            "link_id": 1,
                            "name": "Ethernet0",
                            "nio": "NIO_UDP",
                            "port_number": 0,
                            "adapter_number": 0
                        }
                    ],
                    "properties": {
                        "console": 4501,
                        "name": "VPCS 1",
                        "script_file": "startup.vpc"
                    },
                    "server_id": 1,
                    "type": "VPCSDevice",
                    "vpcs_id": 1,
                    "vm_id": "2b5476de-6e79-4eb5-b0eb-8c54c7821cb8",
                    "x": -349.5,
                    "y": -206.5
                },
                {
                    "description": "VPCS device",
                    "id": 2,
                    "label": {
                        "color": "#000000",
                        "font": "TypeWriter,10,-1,5,75,0,0,0,0,0",
                        "text": "VPCS 2",
                        "x": 10.75,
                        "y": -25.0
                    },
                    "ports": [
                        {
                            "description": "connected to VPCS 1 on port Ethernet0",
                            "id": 2,
                            "link_id": 1,
                            "name": "Ethernet0",
                            "nio": "NIO_UDP",
                            "port_number": 0
                        }
                    ],
                    "properties": {
                        "console": 4502,
                        "name": "VPCS 2",
                        "script_file": "startup.vpc"
                    },
                    "server_id": 1,
                    "type": "VPCSDevice",
                    "vm_id": "2b5476de-6e79-4eb5-b0eb-8c54c7821cba",
                    "vpcs_id": 2,
                    "x": 69.5,
                    "y": -190.5
                }
            ],
            "servers": [
                {
                    "cloud": False,
                    "host": "127.0.0.1",
                    "id": 1,
                    "local": True,
                    "port": 3080
                }
            ]
        },
        "type": "topology",
        "version": "1.3.0"
    }

    monkeypatch.setattr('gns3.main_window.MainWindow.instance', lambda: main_window)

    # We return an uuid for each HTTP post
    def http_loader(self, method, path, callback, body={}, **kwargs):
        if path == "/projects":
            callback({"project_id": uuid.uuid4(), "path": str(tmpdir)})
        elif path[-14:] == "/notifications":
            pass
        else:
            callback({"vm_id": uuid.uuid4()})

    monkeypatch.setattr("gns3.http_client.HTTPClient.createHTTPQuery", http_loader)

    monkeypatch.setattr("gns3.http_client.HTTPClient.connected", lambda self: True)

    topology = Topology()
    topology.project = project
    topology._load(topo)

    assert topology._project.id() == project.id()
    assert len(topology.nodes()) == 2
    assert len(topology._node_to_links_mapping) == 2
    assert topology.getNode(1).initialized()
    assert topology.getNode(1).server() is not None
    assert topology.getNode(2).initialized()
    assert main_window.uiGraphicsView.addLink.called


def test_load_invalid_server(project, monkeypatch, main_window, tmpdir):

    topo = {
        "project_id": project.id(),
        "auto_start": False,
        "name": "twovpcs",
        "topology": {
            "links": [
                {
                    "description": "Link from VPCS 1 port Ethernet0 to VPCS 2 port Ethernet0",
                    "destination_node_id": 2,
                    "destination_port_id": 2,
                    "id": 1,
                    "source_node_id": 1,
                    "source_port_id": 1
                }
            ],
            "nodes": [
                {
                    "description": "VPCS device",
                    "id": 1,
                    "label": {
                        "color": "#000000",
                        "font": "TypeWriter,10,-1,5,75,0,0,0,0,0",
                        "text": "VPCS 1",
                        "x": 10.75,
                        "y": -25.0
                    },
                    "ports": [
                        {
                            "description": "connected to VPCS 2 on port Ethernet0",
                            "id": 1,
                            "link_id": 1,
                            "name": "Ethernet0",
                            "nio": "NIO_UDP",
                            "port_number": 0,
                            "adapter_number": 0
                        }
                    ],
                    "properties": {
                        "console": 4501,
                        "name": "VPCS 1",
                        "script_file": "startup.vpc"
                    },
                    "server_id": 1,
                    "type": "VPCSDevice",
                    "vpcs_id": 1,
                    "vm_id": "2b5476de-6e79-4eb5-b0eb-8c54c7821cb8",
                    "x": -349.5,
                    "y": -206.5
                },
                {
                    "description": "VPCS device",
                    "id": 2,
                    "label": {
                        "color": "#000000",
                        "font": "TypeWriter,10,-1,5,75,0,0,0,0,0",
                        "text": "VPCS 2",
                        "x": 10.75,
                        "y": -25.0
                    },
                    "ports": [
                        {
                            "description": "connected to VPCS 1 on port Ethernet0",
                            "id": 2,
                            "link_id": 1,
                            "name": "Ethernet0",
                            "nio": "NIO_UDP",
                            "port_number": 0
                        }
                    ],
                    "properties": {
                        "console": 4502,
                        "name": "VPCS 2",
                        "script_file": "startup.vpc"
                    },
                    "server_id": 1,
                    "type": "VPCSDevice",
                    "vm_id": "2b5476de-6e79-4eb5-b0eb-8c54c7821cba",
                    "vpcs_id": 2,
                    "x": 69.5,
                    "y": -190.5
                }
            ],
            "servers": [
                {
                    "host": "127.0.0.1",
                    "id": 1,
                    "local": False,
                    "port": 3081
                }
            ]
        },
        "type": "topology",
        "version": "1.3.0"
    }

    monkeypatch.setattr('gns3.main_window.MainWindow.instance', lambda: main_window)

    # We return an uuid for each HTTP post
    def http_loader(self, method, path, callback, body={}, **kwargs):
        if path == "/projects":
            callback({"project_id": uuid.uuid4(), "path": str(tmpdir)})
        elif path[-14:] == "/notifications":
            pass
        else:
            callback({"vm_id": uuid.uuid4()})

    monkeypatch.setattr("gns3.http_client.HTTPClient.createHTTPQuery", http_loader)

    monkeypatch.setattr("gns3.http_client.HTTPClient.connected", lambda self: True)

    topology = Topology()
    topology.project = project
    with patch("gns3.qt.QtWidgets.QMessageBox.warning", return_value=gns3.qt.QtWidgets.QMessageBox.Yes):
        topology._load(topo)

    assert topology._project.id() == project.id()
    assert len(topology.nodes()) == 2
    assert len(topology._node_to_links_mapping) == 2
    assert topology.getNode(1).initialized()
    assert topology.getNode(1).server() is not None
    assert topology.getNode(2).initialized()
    assert main_window.uiGraphicsView.addLink.called


def test_load_1_2_topology(project, monkeypatch, main_window, tmpdir):

    topo = {
        "auto_start": False,
        "name": "twovpcs",
        "topology": {
            "links": [
                {
                    "description": "Link from VPCS 1 port Ethernet0 to VPCS 2 port Ethernet0",
                    "destination_node_id": 2,
                    "destination_port_id": 2,
                    "id": 1,
                    "source_node_id": 1,
                    "source_port_id": 1
                }
            ],
            "nodes": [
                {
                    "description": "VPCS device",
                    "id": 1,
                    "label": {
                        "color": "#000000",
                        "font": "TypeWriter,10,-1,5,75,0,0,0,0,0",
                        "text": "VPCS 1",
                        "x": 10.75,
                        "y": -25.0
                    },
                    "ports": [
                        {
                            "description": "connected to VPCS 2 on port Ethernet0",
                            "id": 1,
                            "link_id": 1,
                            "name": "Ethernet0",
                            "nio": "NIO_UDP",
                            "port_number": 0
                        }
                    ],
                    "properties": {
                        "console": 4501,
                        "name": "VPCS 1",
                        "script_file": "startup.vpc"
                    },
                    "server_id": 1,
                    "type": "VPCSDevice",
                    "vpcs_id": 1,
                    "x": -349.5,
                    "y": -206.5
                },
                {
                    "description": "VPCS device",
                    "id": 2,
                    "label": {
                        "color": "#000000",
                        "font": "TypeWriter,10,-1,5,75,0,0,0,0,0",
                        "text": "VPCS 2",
                        "x": 10.75,
                        "y": -25.0
                    },
                    "ports": [
                        {
                            "description": "connected to VPCS 1 on port Ethernet0",
                            "id": 2,
                            "link_id": 1,
                            "name": "Ethernet0",
                            "nio": "NIO_UDP",
                            "port_number": 0
                        }
                    ],
                    "properties": {
                        "console": 4502,
                        "name": "VPCS 2",
                        "script_file": "startup.vpc"
                    },
                    "server_id": 1,
                    "type": "VPCSDevice",
                    "vpcs_id": 2,
                    "x": 69.5,
                    "y": -190.5
                }
            ],
            "servers": [
                {
                    "cloud": False,
                    "host": "127.0.0.1",
                    "id": 1,
                    "local": True,
                    "port": 3080
                }
            ]
        },
        "type": "topology",
        "version": "1.2.3"
    }

    monkeypatch.setattr('gns3.main_window.MainWindow.instance', lambda: main_window)

    project_call = 0
    # We return an uuid for each HTTP post

    def http_loader(self, method, path, callback, body={}, **kwargs):
        if path == "/projects":
            callback({"project_id": uuid.uuid4(), "path": str(tmpdir)}, error=False, server=local_server)
            project_call += 1
            assert project_call < 2
        elif path[-14:] == "/notifications":
            pass
        else:
            callback({"vm_id": uuid.uuid4()})

    monkeypatch.setattr("gns3.http_client.HTTPClient.createHTTPQuery", http_loader)

    monkeypatch.setattr("gns3.http_client.HTTPClient.connected", lambda self: True)

    topology = Topology()
    topology.project = project
    topology._project.setName("unsaved")
    topology._project.setTopologyFile(str(tmpdir))
    topology.dump = MagicMock()
    topology._load(topo)

    assert topology._project.id() is not None
    assert len(topology.nodes()) == 2
    assert len(topology._node_to_links_mapping) == 2
    assert topology.getNode(1).initialized()
    assert topology.getNode(2).initialized()
    assert main_window.uiGraphicsView.addLink.called
    assert main_window.saveProject.called


def test_image_in_project(tmpdir):
    project_dir = tmpdir / "project" / "project-files"
    os.makedirs(str(project_dir / "images"))

    project = Project()
    project.setFilesDir(str(tmpdir / "project"))

    topology = Topology()
    topology.project = project

    with open(str(project_dir / "images" / "1.jpg"), "w+") as f:
        f.write("AA")

    image1 = PixmapImageItem(None, "images/1.jpg")
    topology.addImage(image1)
    assert image1 in topology._images

    image2 = PixmapImageItem(None, "images/1.jpg")
    topology.addImage(image2)
    assert image1 in topology._images
    assert image2 in topology._images

    topology.removeImage(image2)
    assert os.path.exists(str(project_dir / "images" / "1.jpg"))

    # If not image use this file delete it
    topology.removeImage(image1)
    assert not os.path.exists(str(project_dir / "images" / "1.jpg"))


def test_image_outside_project(tmpdir):
    """
    By security we do not delete image outside project.
    This should not append but if someone reuse the image items for
    something else.
    """

    project_img_dir = tmpdir / "project" / "project-files" / "images"
    os.makedirs(str(project_img_dir))

    project = Project()
    project.setFilesDir(str(tmpdir / "project"))

    topology = Topology()
    topology.project = project

    with open(str(tmpdir / "1.jpg"), "w+") as f:
        f.write("AA")

    image1 = PixmapImageItem(None, str(tmpdir / "1.jpg"))
    topology.addImage(image1)
    assert image1 in topology._images
    topology.removeImage(image1)
    assert os.path.exists(str(tmpdir / "1.jpg"))
