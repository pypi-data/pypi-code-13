"""Example."""

from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import View

import json


class ExampleView(View):
    """Example."""

    def get(self, request):
        """Example."""
        context = {
            'crop_settings': {
                'url': (
                    'http://www.vegan101.info/wp1/wp-content/' +
                    'uploads/baby_pig.jpg'
                ),
                'klass': 'my_cropped_image_class',
                'output_key': 'cute_pig_123',
                'jcrop': dict(
                    aspectRatio=360.0 / 200.0,
                    setSelect=[0, 0, 10000, 10000],
                ),
            },
        }
        return render(request, 'django_litecrop/example.html', context)

    def post(self, request):
        """
        Return something like the following.

        {
            "h": 156.11111111111111,
            "x2": 348,
            "natural_height": 515,
            "w": 281,
            "natural_width": 1440,
            "y": 9,
            "x": 67,
            "display_height": 200,
            "y2": 165.11111111111111,
            "display_width": 559
        }
        """
        return JsonResponse(
            json.loads(request.POST['cute_pig_123'])
        )
