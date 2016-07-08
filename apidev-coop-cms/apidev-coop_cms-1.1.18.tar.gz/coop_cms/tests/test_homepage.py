# -*- coding: utf-8 -*-

from django.conf import settings

from unittest import skipIf

from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.test.utils import override_settings

from model_mommy import mommy

from coop_cms.models import BaseArticle, SiteSettings
from coop_cms.settings import get_article_class, cms_no_homepage
from coop_cms.shortcuts import get_headlines
from coop_cms.tests import BaseTestCase, UserBaseTestCase, BeautifulSoup


@override_settings(COOP_CMS_NO_HOMEPAGE=False)
class NoHomepageTest(UserBaseTestCase):
    
    @override_settings(COOP_CMS_NO_HOMEPAGE=True)
    def test_view_article_set_homepage_no_homepage(self):
        self._log_as_editor(can_add=True)
        article_class = get_article_class()
        art = mommy.make(article_class, is_homepage=False, publication=BaseArticle.PUBLISHED)
        url = art.get_edit_url()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content)
        url = reverse('coop_cms_set_homepage', args=[art.id])
        links = soup.select(".coop-bar a[href={0}]".format(url))
        self.assertEqual(0, len(links))
        
    def test_view_article_set_homepage(self):
        self._log_as_editor(can_add=True)
        article_class = get_article_class()
        art = mommy.make(article_class, is_homepage=False, publication=BaseArticle.PUBLISHED)
        url = art.get_edit_url()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        soup = BeautifulSoup(response.content)
        url = reverse('coop_cms_set_homepage', args=[art.id])
        links = soup.select(".coop-bar a[href={0}]".format(url))
        self.assertEqual(1, len(links))


@skipIf(cms_no_homepage(), "no homepage")
class HomepageTest(UserBaseTestCase):
    
    def setUp(self):
        super(HomepageTest, self).setUp()
        self.site_id = settings.SITE_ID

    def tearDown(self):
        super(HomepageTest, self).tearDown()
        settings.SITE_ID = self.site_id
        
    def test_user_settings_homepage(self):
        site = Site.objects.get(id=settings.SITE_ID)
        a1 = get_article_class().objects.create(title="python", content='python')
        site_settings = mommy.make(SiteSettings, site=site, homepage_url=a1.get_absolute_url())
    
        response = self.client.get(reverse('coop_cms_homepage'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response['Location'].find(a1.get_absolute_url()) >= 0)
            
    def test_user_settings_homepage_priority(self):
        site = Site.objects.get(id=settings.SITE_ID)
        a1 = get_article_class().objects.create(title="python", content='python')
        a2 = get_article_class().objects.create(title="django", content='django', homepage_for_site=site)
        site_settings = mommy.make(SiteSettings, site=site, homepage_url=a1.get_absolute_url())
    
        response = self.client.get(reverse('coop_cms_homepage'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response['Location'].find(a1.get_absolute_url()) >= 0)
    
    def test_user_settings_homepage_not_set(self):
        site = Site.objects.get(id=settings.SITE_ID)
        a1 = get_article_class().objects.create(title="python", content='python')
        a2 = get_article_class().objects.create(title="django", content='django', homepage_for_site=site)
        site_settings = mommy.make(SiteSettings, site=site, homepage_url="")

        response = self.client.get(reverse('coop_cms_homepage'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response['Location'].find(a2.get_absolute_url()) < 0)
        self.assertTrue(response['Location'].find(reverse('coop_cms_view_all_articles')) >= 0)

    def test_view_change_homepage(self):
        self._log_as_editor()
        a1 = get_article_class().objects.create(title="python", content='python')
        
        response = self.client.get(reverse('coop_cms_set_homepage', args=[a1.id]))
        self.assertEqual(response.status_code, 200)
        
        a1 = get_article_class().objects.get(id=a1.id)
        self.assertEqual(a1.is_homepage, False)
    
    def test_change_homepage(self):
        self._log_as_editor()
        site = Site.objects.get(id=settings.SITE_ID)
        a1 = get_article_class().objects.create(title="python", content='python')
        a2 = get_article_class().objects.create(title="django", content='django')
        a3 = get_article_class().objects.create(title="home1", content='homepage1')
        
        response = self.client.post(reverse('coop_cms_set_homepage', args=[a2.id]), data={'confirm': '1'})
        self.assertEqual(response.status_code, 200)
        a2 = get_article_class().objects.get(id=a2.id)
        home_url = reverse("coop_cms_homepage")
        self.assertEqual(response.content,
            '<script>$.colorbox.close(); window.location="{0}";</script>'.format(home_url))
        self.assertEqual(a2.homepage_for_site, None)
        site_settings = SiteSettings.objects.get(site__id=settings.SITE_ID)
        self.assertEqual(site_settings.homepage_url, a2.get_absolute_url())
        
        response = self.client.post(reverse('coop_cms_set_homepage', args=[a3.id]), data={'confirm': '1'})
        self.assertEqual(response.status_code, 200)
        home_url = reverse("coop_cms_homepage")
        self.assertEqual(response.content,
            '<script>$.colorbox.close(); window.location="{0}";</script>'.format(home_url)
        )
        a2 = get_article_class().objects.get(id=a2.id)
        a3 = get_article_class().objects.get(id=a3.id)
        site_settings = SiteSettings.objects.get(site__id=settings.SITE_ID)
        self.assertEqual(site_settings.homepage_url, a3.get_absolute_url())

        self.assertEqual(a2.homepage_for_site, None)
        self.assertEqual(a3.homepage_for_site, None)
    
    def test_change_homepage_anonymous(self):
        Site.objects.get(id=settings.SITE_ID)
        a1 = get_article_class().objects.create(title="python", content='python')
        a2 = get_article_class().objects.create(title="django", content='django')
        a3 = get_article_class().objects.create(title="home1", content='homepage1')
        
        response = self.client.post(reverse('coop_cms_set_homepage', args=[a2.id]), data={'confirm': '1'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.redirect_chain[0][0], 302)
        self.assertTrue(response.redirect_chain[-1][0].find(reverse('django.contrib.auth.views.login')) >= 0)
        a2 = get_article_class().objects.get(id=a2.id)
        self.assertEqual(a2.homepage_for_site, None)
        self.assertEqual(0, SiteSettings.objects.count())

    def test_change_homepage_multisites(self):
        self._log_as_editor()
        site1 = Site.objects.get(id=settings.SITE_ID)
        site2 = Site.objects.create(domain="wooooooaa.com", name="wooaa")
        
        a1 = get_article_class().objects.create(title="python", content='python')
        a2 = get_article_class().objects.create(title="django", content='django')
        a3 = get_article_class().objects.create(title="home1", content='homepage1')
        
        settings.SITE_ID = site2.id
        a4 = get_article_class().objects.create(title="home1", content='homepage2')
        
        settings.SITE_ID = site1.id
        response = self.client.post(reverse('coop_cms_set_homepage', args=[a3.id]), data={'confirm': '1'})
        home_url = reverse("coop_cms_homepage")
        self.assertEqual(response.content,
            '<script>$.colorbox.close(); window.location="{0}";</script>'.format(home_url)
        )
        site_settings1 = SiteSettings.objects.get(site=site1)
        self.assertEqual(site_settings1.homepage_url, a3.get_absolute_url())

        settings.SITE_ID = site2.id
        response = self.client.post(reverse('coop_cms_set_homepage', args=[a4.id]), data={'confirm': '1'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content,
            '<script>$.colorbox.close(); window.location="{0}";</script>'.format(home_url)
        )
        a4 = get_article_class().objects.get(id=a4.id)
        a3 = get_article_class().objects.get(id=a3.id)

        site_settings1 = SiteSettings.objects.get(site=site1)
        self.assertEqual(site_settings1.homepage_url, a3.get_absolute_url())

        site_settings2 = SiteSettings.objects.get(site=site2)
        self.assertEqual(site_settings2.homepage_url, a4.get_absolute_url())

    def test_homepage_multisites(self):
        site1 = Site.objects.get(id=settings.SITE_ID)
        site2 = Site.objects.create(domain="wooooooaa.com", name="wooaa")
        
        article1 = get_article_class().objects.create(title="python", content='python')
        article2 = get_article_class().objects.create(title="django", content='django')
        article3 = get_article_class().objects.create(title="home1", content='homepage1')
        article4 = get_article_class().objects.create(title="home2", content='homepage2')

        self.assertEqual(0, SiteSettings.objects.count())

        SiteSettings.objects.create(site=site1, homepage_url=article3.get_absolute_url())

        SiteSettings.objects.create(site=site2, homepage_url=article4.get_absolute_url())

        settings.SITE_ID = site1.id
        response = self.client.get(reverse('coop_cms_homepage'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response['Location'].find(article3.get_absolute_url()) >= 0)
        self.assertEqual(article3.is_homepage, True)
        self.assertEqual(article4.is_homepage, False)

    def test_homepage_multisites_same_home(self):
        site1 = Site.objects.get(id=settings.SITE_ID)
        site2 = Site.objects.create(domain="wooooooaa.com", name="wooaa")

        article1 = get_article_class().objects.create(title="python", content='python')
        article2 = get_article_class().objects.create(title="django", content='django')
        article3 = get_article_class().objects.create(title="home1", content='homepage1')
        article4 = get_article_class().objects.create(title="home2", content='homepage2')

        self.assertEqual(0, SiteSettings.objects.count())

        SiteSettings.objects.create(site=site1, homepage_url=article3.get_absolute_url())

        SiteSettings.objects.create(site=site2, homepage_url=article3.get_absolute_url())

        settings.SITE_ID = site1.id
        response = self.client.get(reverse('coop_cms_homepage'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response['Location'].find(article3.get_absolute_url()) >= 0)
        self.assertEqual(article3.is_homepage, True)
        self.assertEqual(article4.is_homepage, False)

        settings.SITE_ID = site2.id
        response = self.client.get(reverse('coop_cms_homepage'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response['Location'].find(article3.get_absolute_url()) >= 0)
        self.assertEqual(article3.is_homepage, True)
        self.assertEqual(article4.is_homepage, False)


class HeadlineTest(BaseTestCase):

    def test_get_headlines_no_edit_perms(self):
        article_class = get_article_class()
        article1 = mommy.make(article_class, publication=BaseArticle.PUBLISHED, headline=True)
        article2 = mommy.make(article_class, publication=BaseArticle.DRAFT, headline=True)
        article3 = mommy.make(article_class, publication=BaseArticle.PUBLISHED, headline=False)
        article4 = mommy.make(article_class, publication=BaseArticle.DRAFT, headline=False)
        article5 = mommy.make(article_class, publication=BaseArticle.ARCHIVED, headline=True)
        article6 = mommy.make(article_class, publication=BaseArticle.ARCHIVED, headline=False)

        homepage = mommy.make(article_class, publication=BaseArticle.PUBLISHED, headline=False)
        site = Site.objects.get_current()
        SiteSettings.objects.create(site=site, homepage_url=homepage.get_absolute_url())

        headlines = list(get_headlines(homepage))
        self.assertEqual([article1], headlines)

    def test_get_headlines_edit_perms(self):
        article_class = get_article_class()
        article1 = mommy.make(article_class, publication=BaseArticle.PUBLISHED, headline=True)
        article2 = mommy.make(article_class, publication=BaseArticle.DRAFT, headline=True)
        article3 = mommy.make(article_class, publication=BaseArticle.PUBLISHED, headline=False)
        article4 = mommy.make(article_class, publication=BaseArticle.DRAFT, headline=False)
        article5 = mommy.make(article_class, publication=BaseArticle.ARCHIVED, headline=True)
        article6 = mommy.make(article_class, publication=BaseArticle.ARCHIVED, headline=False)

        homepage = mommy.make(article_class, publication=BaseArticle.PUBLISHED, headline=False)
        site = Site.objects.get_current()
        SiteSettings.objects.create(site=site, homepage_url=homepage.get_absolute_url())

        headlines = list(get_headlines(homepage, editable=True))
        self.assertEqual(sorted([article1, article2], key=lambda x: x.id), sorted(headlines, key=lambda x: x.id))

    def test_get_headlines_not_homepage(self):
        article_class = get_article_class()
        article1 = mommy.make(article_class, publication=BaseArticle.PUBLISHED, headline=True)
        article2 = mommy.make(article_class, publication=BaseArticle.DRAFT, headline=True)
        article3 = mommy.make(article_class, publication=BaseArticle.PUBLISHED, headline=False)
        article4 = mommy.make(article_class, publication=BaseArticle.DRAFT, headline=False)
        article5 = mommy.make(article_class, publication=BaseArticle.ARCHIVED, headline=True)
        article6 = mommy.make(article_class, publication=BaseArticle.ARCHIVED, headline=False)

        not_homepage = mommy.make(article_class, publication=BaseArticle.PUBLISHED, headline=False)

        headlines = list(get_headlines(not_homepage))
        self.assertEqual([], headlines)

    def test_get_headlines_other_homepage(self):
        article_class = get_article_class()
        article1 = mommy.make(article_class, publication=BaseArticle.PUBLISHED, headline=True)
        article2 = mommy.make(article_class, publication=BaseArticle.DRAFT, headline=True)
        article3 = mommy.make(article_class, publication=BaseArticle.PUBLISHED, headline=False)
        article4 = mommy.make(article_class, publication=BaseArticle.DRAFT, headline=False)
        article5 = mommy.make(article_class, publication=BaseArticle.ARCHIVED, headline=True)
        article6 = mommy.make(article_class, publication=BaseArticle.ARCHIVED, headline=False)

        other_homepage = mommy.make(article_class, publication=BaseArticle.PUBLISHED, headline=False)

        site = mommy.make(Site)
        SiteSettings.objects.create(site=site, homepage_url=other_homepage.get_absolute_url())

        headlines = list(get_headlines(other_homepage))
        self.assertEqual([], headlines)

    def test_get_headlines_other_site(self):
        article_class = get_article_class()
        article1 = mommy.make(article_class, publication=BaseArticle.PUBLISHED, headline=True)
        article2 = mommy.make(article_class, publication=BaseArticle.PUBLISHED, headline=True)
        article3 = mommy.make(article_class, publication=BaseArticle.PUBLISHED, headline=True)

        other_site = mommy.make(Site)
        article2.sites.clear()
        article2.sites.add(other_site)
        article2.save()

        article3.sites.clear()
        article3.save()

        homepage = mommy.make(article_class, publication=BaseArticle.PUBLISHED, headline=False)
        site = Site.objects.get_current()
        SiteSettings.objects.create(site=site, homepage_url=homepage.get_absolute_url())

        headlines = list(get_headlines(homepage))
        self.assertEqual([article1], headlines)
