_2_MB = 2048000

SUMMERNOTE_DEFAULT_CONFIG = {

    'restrict_to_user': False,
    'use_path_user': False,
    'upload_only_image_files': False,
    'maximum_image_upload': _2_MB,

    'assets': {
        'js': (
            'https://code.jquery.com/jquery-2.2.4.min.js',
            'https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js',
            'https://cdnjs.cloudflare.com/ajax/libs/summernote/0.8.1/summernote.min.js', ),

        'css': {
            'all': (
                'https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css',
                'https://cdnjs.cloudflare.com/ajax/libs/summernote/0.8.1/summernote.css',
            )
        }
    },

    'editors': {
        'default': {
            'airMode': False,
            'toolbar': [
                ['style', ['bold', 'italic', 'underline', 'clear']],
                ['font', ['strikethrough', 'superscript', 'subscript']],
                ['fontsize', ['fontsize']],
                ['color', ['color']],
                ['para', ['ul', 'ol', 'paragraph']],
                ['height', ['height']]
            ],
            'popover': {
                'air':[
                    ['para', ['ul', 'ol', 'paragraph']],
                ]
            }
        },

    }
}