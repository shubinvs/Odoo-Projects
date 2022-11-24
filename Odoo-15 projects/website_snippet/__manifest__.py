{
    'name': 'WEBSITE SNIPPETS',
    'application': True,
    'sequence': '4',
    'author': 'SHUBIN V S',
    'version': '15.0.1.0.0',
    'depends': ['base', 'website', 'website_blog'],
    'data': [
        'views/snippet.xml'
    ],
    'assets': {
        'web.assets_frontend': [
            'website_snippet/static/src/js/snippet.js'
        ]
    }
}
