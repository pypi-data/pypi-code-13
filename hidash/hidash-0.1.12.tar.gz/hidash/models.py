from django.db import models


FREQUENCY = ((0, 'Daily'),
             (1, 'Weekly'),
             (2, 'Monthly'),
             (3, 'Yearly'))


class Chart(models.Model):
    '''
    Holds the configuration of a chart
    '''
    name = models.CharField(max_length=25, unique=True)
    library = models.CharField(max_length=15)
    dimension = models.CharField(max_length=50)
    chart_type = models.CharField(max_length=15, null=True, blank=True)
    query = models.TextField(max_length=10000)
    send_report_in_email = models.BooleanField(default=False)
    frequency = models.IntegerField(choices=FREQUENCY, null=True)

    def __unicode__(self):
        return self.name


class ChartGroup(models.Model):
    '''
    Holds the Group names for grouping multiple charts under that group
    '''
    name = models.CharField(max_length=25)
    chart = models.ForeignKey(Chart)

    def __unicode__(self):
        return self.name


class ChartMetric(models.Model):
    '''
    One to many mapping to hold the metrics of a chart
    '''
    chart = models.ForeignKey(Chart, related_name='chart')
    metric = models.CharField(max_length=50)

    def __unicode__(self):
        return self.metric


class ChartAuthGroup(models.Model):
    '''
    One to many mapping to hold the chart_groups permitted to view the chart
    '''
    chart = models.ForeignKey(Chart)
    auth_group = models.CharField(max_length=50)

    def __unicode__(self):
        return self.chart_group


class ChartAuthPermission(models.Model):
    '''
    One to many mapping to hold the needed permissions to view the chart
    '''
    chart = models.ForeignKey(Chart)
    permission = models.CharField(max_length=50)

    def __unicode__(self):
        return self.permission
