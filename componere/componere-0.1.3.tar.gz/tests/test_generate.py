from unittest import TestCase
import generate
import datetime


class GenerateTest(TestCase):
	def test_invalid_usage(self):
		self.assertEqual(2, generate._main(["foo"]))
		for command in ["detail", "overview", "areas", "all"]:
			self.assertEqual(3, generate._main([command]))

		self.assertEqual(4, generate._main(["area"]))
		self.assertEqual(4, generate._main(["area", "foo"]))

	def test_areas_parsing(self):
		areas = generate._load_areas("test_areas.yaml")
		self.assertEqual(3, len(areas))

		empty = areas.get("partial")
		self.assertNotEqual(None, empty)
		self.assertEqual(u"Partial", empty.name)
		self.assertEqual(None, empty.parent_identifier)

		all = areas.get("all")
		self.assertNotEqual(None, all)
		self.assertEqual(u"All", all.name)
		self.assertEqual("partial", all.parent_identifier)

	def test_levels_parsing(self):
		levels = generate._load_levels("test_levels.yaml")
		self.assertEqual(2, len(levels))

		level10 = levels.get("level-10")
		self.assertNotEqual(None, level10)
		self.assertEqual(u"Level 10", level10.name)
		self.assertEqual(10, level10.order)

	def test_teams_parsing(self):
		teams = generate._load_teams("test_teams.yaml")
		self.assertEqual(2, len(teams))

		team1 = teams.get("team-1")
		self.assertNotEqual(None, team1)
		self.assertEqual(u"Team 1 Contact", team1.name)
		self.assertNotEqual(None, team1.team_contact)
		self.assertEqual("team-1@foo.com", team1.team_contact.email)
		self.assertEquals(None, team1.team_contact.name)
		self.assertNotEqual(None, team1.lead_contact)
		self.assertEquals(u"Lead Contact", team1.lead_contact.name)
		self.assertEquals("lead-1@foo.com", team1.lead_contact.email)
		self.assertNotEqual(None, team1.display)
		self.assertEquals("#218041", team1.display.background_color)
		self.assertEquals("#ffffff", team1.display.foreground_color)

	def test_components_parsing(self):
		components = generate._load_components("test_components.yaml")
		self.assertEqual(2, len(components))

		root = components.get("root")
		self.assertNotEqual(None, root)
		self.assertEqual(u"Root", root.name)
		self.assertEqual("level-10", root.level_identifier)
		self.assertEqual("apk", root.type)
		self.assertEqual("team-1", root.team_identifier)
		self.assertEqual("partial", root.area_identifier)
		self.assertEqual(u"The Root Application", root.description)
		self.assertEqual("git@github.com:lolay/investigo-android.git", root.git)
		self.assertEqual(datetime.date(2016, 04, 14), root.release_date)
		self.assertEqual(["dependency"], root.dependency_identifiers)
