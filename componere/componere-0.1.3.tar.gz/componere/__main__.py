#!/usr/bin/env python

import sys
import os
import yaml
from graphviz import Digraph

class Area:
	identifier = None
	name = None
	parent_identifier = None

	def __init__(self, identifier, name=None, parent_identifier=None):
		self.identifier = identifier
		self.name = name
		self.parent_identifier = parent_identifier

	@classmethod
	def from_values_dict(cls, identifier, values_dict):
		if values_dict is None:
			return None
		identifier = identifier
		name = values_dict.get("name")
		parent_identifier = values_dict.get("parent")
		return Area(identifier, name, parent_identifier)

	@classmethod
	def from_collection_dict(cls, collection_dict):
		if collection_dict is None:
			return None

		dict = {}
		for identifier, values_dict in collection_dict.iteritems():
			object = Area.from_values_dict(identifier, values_dict)
			dict[identifier] = object
		return dict


class Level:
	identifier = None
	order = None
	name = None

	def __init__(self, identifier, order=None, name=None):
		self.identifier = identifier
		self.order = order
		self.name = name

	@classmethod
	def from_values_dict(cls, identifier, values_dict):
		if values_dict is None:
			return None
		order = values_dict.get("order")
		name = values_dict.get("name")
		return Level(identifier, order, name)

	@classmethod
	def from_collection_dict(cls, collection_dict):
		if collection_dict is None:
			return None

		dict = {}
		for identifier, values_dict in collection_dict.iteritems():
			object = Level.from_values_dict(identifier, values_dict)
			dict[identifier] = object
		return dict


class Contact:
	name = None
	email = None

	def __init__(self, name=None, email=None):
		self.name = name
		self.email = email

	@classmethod
	def from_values_dict(cls, values_dict):
		if values_dict is None:
			return None
		name = values_dict.get("name")
		email = values_dict.get("email")
		return Contact(name, email)


class Display:
	background_color = None
	foreground_color = None

	def __init__(self, background_color=None, foreground_color=None):
		self.background_color = background_color
		self.foreground_color = foreground_color

	@classmethod
	def from_values_dict(cls, values_dict):
		if values_dict is None:
			return None
		background_color = values_dict.get("background-color")
		foreground_color = values_dict.get("foreground-color")
		return Display(background_color, foreground_color)


class Team:
	identifier = None
	name = None
	team_contact = None
	lead_contact = None
	display = None

	def __init__(
		self,
		identifier,
		name=None,
		team_contact=None,
		lead_contact=None,
		display=None
	):
		self.identifier = identifier
		self.name = name
		self.team_contact = team_contact
		self.lead_contact = lead_contact
		self.display = display

	@classmethod
	def from_values_dict(cls, identifier, values_dict):
		if values_dict is None:
			return None
		name = values_dict.get("name")
		team_contact = Contact.from_values_dict(values_dict.get("team-contact"))
		lead_contact = Contact.from_values_dict(values_dict.get("lead-contact"))
		display = Display.from_values_dict(values_dict.get("display"))
		return Team(identifier, name, team_contact, lead_contact, display)

	@classmethod
	def from_collection_dict(cls, collection_dict):
		if collection_dict is None:
			return None

		dict = {}
		for identifier, values_dict in collection_dict.iteritems():
			object = Team.from_values_dict(identifier, values_dict)
			dict[identifier] = object
		return dict

class Component:
	identifier = None
	name = None
	level_identifier = None
	type = None
	team_identifier = None
	area_identifier = None
	description = None
	git = None
	release_date = None
	dependency_identifiers = None

	def __init__(
		self,
		identifier,
		name=None,
		level_identifier=None,
		type=None,
		team_identifier=None,
		area_identifier=None,
		description=None,
		git=None,
		release_date=None,
		dependency_identifiers=None
	):
		self.identifier = identifier
		self.name = name
		self.level_identifier = level_identifier
		self.type = type
		self.team_identifier = team_identifier
		self.area_identifier = area_identifier
		self.description = description
		self.git = git
		self.release_date = release_date
		self.dependency_identifiers = dependency_identifiers

	@classmethod
	def from_values_dict(cls, identifier, values_dict):
		if values_dict is None:
			return None
		name = values_dict.get("name")
		level = values_dict.get("level")
		type = values_dict.get("type")
		team_identifier = values_dict.get("team")
		area_identifier = values_dict.get("area")
		description = values_dict.get("description")
		git = values_dict.get("git")
		release_date = values_dict.get("release-date")
		dependency_identifiers = values_dict.get("dependencies")

		return Component(
			identifier,
			name,
			level,
			type,
			team_identifier,
			area_identifier,
			description,
			git,
			release_date,
			dependency_identifiers
		)

	@classmethod
	def from_collection_dict(cls, collection_dict):
		if collection_dict is None:
			return None

		dict = {}
		for identifier, values_dict in collection_dict.iteritems():
			object = Component.from_values_dict(identifier, values_dict)
			dict[identifier] = object
		return dict


def _load_areas(file):
	if not os.path.isfile(file):
		raise Exception("File {0} is not found".format(file))

	file = open(file)
	areas_dict = yaml.safe_load(file)
	file.close()

	if areas_dict is None:
		return None

	return Area.from_collection_dict(areas_dict)


def _load_levels(file):
	if not os.path.isfile(file):
		raise Exception("File {0} is not found".format(file))

	file = open(file)
	dict = yaml.safe_load(file)
	file.close()

	if dict is None:
		return None

	return Level.from_collection_dict(dict)


def _load_teams(file):
	if not os.path.isfile(file):
		raise Exception("File {0} is not found".format(file))

	file = open(file)
	dict = yaml.safe_load(file)
	file.close()

	if dict is None:
		return None

	return Team.from_collection_dict(dict)


def _load_components(file):
	if not os.path.isfile(file):
		raise Exception("File {0} is not found".format(file))

	file = open(file)
	dict = yaml.safe_load(file)
	file.close()

	if dict is None:
		return None

	return Component.from_collection_dict(dict)


def _find_child_areas(areas, parent_area_identifier):
	found_areas = []
	for area in areas.values():
		#Source
		if parent_area_identifier is None and area.parent_identifier is None:
			found_areas.append(area)
		#Child
		elif area.parent_identifier == parent_area_identifier:
			found_areas.append(area)
	return found_areas


def _find_area_components(components, area_identifier):
	found_components = {}
	for component_identifier, component in components.iteritems():
		if area_identifier is None and component.area_identifier is None:
			found_components[component_identifier] = component
		elif component.area_identifier == area_identifier:
			found_components[component_identifier] = component
	return found_components


def _draw_node_label_table(teams, component):
	node_label = '<<TABLE BORDER="0" CELLSPACING="0" CELLPADDING="4" BGCOLOR="'
	node_label += teams[component.team_identifier].display.background_color
	node_label += '"><TR><TD BORDER="1"><FONT POINT-SIZE="13">'
	node_label += '&lt;&lt;' + component.type + '&gt;&gt;<BR/>'
	node_label += component.name + '</FONT></TD></TR>'
	node_label += '<TR><TD BORDER="1" BALIGN="LEFT">'
	node_label += '+&nbsp;' + component.level_identifier + '&nbsp;:&nbsp;level'

	# For adding more attributes to the node
	if component.release_date is not None:
		node_label += '<BR/>+&nbsp;' + component.release_date.strftime('%m/%d/%Y')
		node_label += '&nbsp;:&nbsp;release date'

	node_label += '</TD></TR></TABLE>>'
	return node_label


def _add_area_with_components_inside(area, area_components, teams, highlited_area_identifier=None):
	digraph = Digraph("cluster_area_" + area.identifier)
	digraph.body.append("label = " + '"' + area.name + '"')
	digraph.body.append('style=bold labeljust="l" fontsize="20"')
	if highlited_area_identifier == area.identifier:
		digraph.body.append('style="filled, bold" fillcolor=lightgrey')
	for component in area_components.values():
		digraph.node(
			component.identifier,
			label=_draw_node_label_table(teams, component),
			fontname="Bitstream Vera Sans",
			fontsize="12",
			shape="plaintext",
			fontcolor=teams[component.team_identifier].display.foreground_color,
		)
	return digraph


def _add_detail_area_components_digraph(
	digraph,
	areas,
	components,
	teams,
	area=None,
	highlited_area_identifier=None,
	depth=1,
):
	if depth > 100:
		raise Exception("Too many recursions")

	parent_digraph = None
	if digraph is not None:
		parent_digraph = digraph
	else:
		parent_digraph = _add_area_with_components_inside(
			area,
			_find_area_components(components, area.identifier),
			teams,
			highlited_area_identifier,
		)

	for child_area in _find_child_areas(
		areas, area.identifier if area is not None else None
	):
		parent_digraph.subgraph(_add_detail_area_components_digraph(
			None,
			areas,
			components,
			teams,
			child_area,
			highlited_area_identifier,
			depth + 1,
		))

	return parent_digraph


def _add_components_edges_digraph(digraph, components):
	for component in components.values():
		if component.dependency_identifiers is not None:
			for dependency_identifier in component.dependency_identifiers:
				#only add edges between pre-existed nodes
				if dependency_identifier in components:
					digraph.edge(component.identifier, dependency_identifier,
						arrowhead='open', style="dashed"
					)

def _add_teams_color_map(parent_digraph, teams):
	color_map = Digraph("cluster_area.teams_color_map")
	color_map.body.append('label = "Teams Colors Map"')
	color_map.body.append('labeljust="l" fontsize="20"')
	for team_identifier, team in teams.iteritems():
		color_map.node(
			team_identifier,
			label=team.name,
			style='filled',
			color=team.display.background_color,
			fontcolor=team.display.foreground_color,
		)
	parent_digraph.subgraph(color_map)


def _build_detail_digraph(
	name,
	output_file,
	areas,
	components,
	teams
):
	root = Digraph(name, filename=output_file, format="png")
	_add_detail_area_components_digraph(root, areas, components, teams)
	_add_components_edges_digraph(root, components)
	_add_teams_color_map(root, _find_showed_teams(components, teams))
	root.view()


def _find_recursive_components_within_area(
	components,
	areas,
	area_identifier,
	depth=1,
):
	if depth > 100:
		raise Exception("Too many recursions")

	found_components = _find_area_components(components, area_identifier)
	for child_area in _find_child_areas(areas, area_identifier):
		found_components.update(_find_recursive_components_within_area(
			components,
			areas,
			child_area.identifier,
			depth + 1,
		))

	return found_components


def _find_direct_connected_components(components, component_group):
	connected_components = {}
	#In Edges
	for component_identifier, component in components.iteritems():
		if component.dependency_identifiers is not None:
			for dependency_identifier in component.dependency_identifiers:
				if dependency_identifier in component_group:
					connected_components[component_identifier] = component
					break
	#Out Edges
	for component in component_group.values():
		if component.dependency_identifiers is not None:
			for dependency_identifier in component.dependency_identifiers:
					connected_components[dependency_identifier] = components[dependency_identifier]

	return connected_components


def _find_showed_teams(showed_components, teams):
	showed_teams = {}
	for component in showed_components.values():
		showed_teams[component.team_identifier] = teams[component.team_identifier]
	return showed_teams


def _add_specific_area_digraph(
	digraph,
	areas,
	area,
	components,
	teams,
	highlited_area_identifier=None,
):
	area_recursive_components = _find_recursive_components_within_area(
		components,
		areas,
		area.identifier
	)
	showed_components = area_recursive_components
	showed_components.update(_find_direct_connected_components(
		components,
		area_recursive_components,
	))
	_add_detail_area_components_digraph(
		digraph,
		areas,
		showed_components,
		teams,
		None,
		highlited_area_identifier,
	)
	_add_components_edges_digraph(digraph, showed_components)
	_add_teams_color_map(digraph, _find_showed_teams(showed_components, teams))


def _build_area_digraph(
	output_file,
	areas,
	components,
	teams,
	specific_area_identifier=None,
):
	for area_identifier, area in areas.iteritems():
		if specific_area_identifier is None or specific_area_identifier == area_identifier:
			root = Digraph(area_identifier, filename=output_file+area_identifier, format="png")
			_add_specific_area_digraph(root, areas, area, components, teams, area_identifier)
			root.view()

def _get_components_for_level(components, levels, level_order):
	level_components = {}
	for component in components.values():
		if levels[component.level_identifier].order >= level_order:
			level_components[component.identifier] = component
	return level_components

def _add_component_edges(digraph, component, all_components, components, parent=None):
	if component.dependency_identifiers is not None:
		for dependency_identifier in component.dependency_identifiers:
			if dependency_identifier in components:
				if parent is None:
					digraph.edge(component.identifier, dependency_identifier,
						arrowhead='open', style="dashed"
					)
				else:
					digraph.edge(parent.identifier, dependency_identifier,
						arrowhead='open', style="dashed", label="\<\<transitive\>\>"
					)
			else:
				_add_component_edges(
					digraph, all_components[dependency_identifier],
					all_components, components, component
				)

def _build_overview_digraph(name, output_file, areas, components, levels, teams, level_order):
	root = Digraph(name, filename=output_file, format="png")
	overview_components = _get_components_for_level(components, levels, level_order)
	_add_detail_area_components_digraph(root, areas, overview_components, teams)
	for component in overview_components.values():
		_add_component_edges(root, component, components, overview_components)
	_add_teams_color_map(root, _find_showed_teams(overview_components, teams))
	root.view()

def _print_usage():
	print "Usage:"
	print "  generate.py detail <directory>"
	print "    Generates a Detail Diagram detail.png and detail.html into the <directory>"
	print "  generate.py overview <level_order> <directory>"
	print "    Generates an Overview diagram overview.png and overview.html into the <directory>"
	print "  generate.py area <area> <directory>"
	print "    Generates an Area diagram <area>.png and <area>.html into the <directory>"
	print "  generate.py areas <directory>"
	print "    Generates all Area diagrams areas.png and area.html into the <directory> and every area"
	print "    into <directory>/areas/<area>.png <area>.html"
	print "  generate.py all <directory>"
	print "    Invokes detail, overview, areas all to the <directory>"


def _main(argv=sys.argv[1:]):
	if len(argv) < 1:
		return _main(["all", "wiki"])

	command = argv[0]

	valid_commands = ["detail", "overview", "areas", "all", "area"]
	if command not in valid_commands:
		_print_usage()
		print "ERROR: Command not one of {0}".format(valid_commands)
		return 2

	directory = None
	def_directory = "system/"
	areas_file = def_directory + "areas.yaml"
	components_file = def_directory + "components.yaml"
	levels_file = def_directory + "levels.yaml"
	teams_file = def_directory + "teams.yaml"

	if command in ["detail", "areas", "all"]:
		if len(argv) != 2:
			_print_usage()
			print "ERROR: Output directory not given"
			return 3
		directory = argv[1]

	level_order = 50
	if command == "overview":
		if len(argv) < 2:
			_print_usage()
			print "ERROR: Output directory not given"
			return 3
		if len(argv) == 3 and argv[1].isdigit():
			level_order = int(argv[1])
		directory = argv[len(argv) - 1]

	area = None
	if command == "area":
		if len(argv) != 3:
			_print_usage()
			print "ERROR: Area and/or directory not given"
			return 4
		area = argv[1]
		directory = argv[2]

	if not os.path.isdir(directory):
		os.mkdir(directory)

	areas = _load_areas(areas_file)
	components = _load_components(components_file)
	teams = _load_teams(teams_file)

	if command in ["detail", "all"]:
		_build_detail_digraph(
			"Detail",
			directory + "/detail",
			areas,
			components,
			teams
		)

	if command in ["overview", "all"]:
		_build_overview_digraph(
			"Overview",
			directory + "/overview",
			areas,
			components,
			_load_levels(levels_file),
			teams,
			level_order
		)

	if command in ["area", "areas", "all"]:
		_build_area_digraph(
			directory + "/areas/",
			areas,
			components,
			teams,
			area
		)

	return 0


if __name__ == "__main__":
	sys.exit(_main(sys.argv[1:]))
