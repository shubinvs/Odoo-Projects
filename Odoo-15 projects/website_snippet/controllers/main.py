from odoo import http
from odoo.http import request
import json


class DynamicSnippet(http.Controller):
    @http.route(['/online_snippets'], type="json", auth="public")
    def online_snippet(self):
        blog = request.env['blog.post'].sudo().search([],
                                                      order='post_date desc',
                                                      limit=8)
        blog_list1 = []
        blog_list2 = []
        for rec in blog:
            blog_name = rec.name
            background = json.loads(rec.cover_properties)
            blog_image = background['background-image'][5:-2]
            blog_url = rec.website_url
            blog_subtitle = rec.subtitle
            if len(blog_list1) < 4:
                blog_list1.append([blog_name, blog_image,
                                   blog_url, blog_subtitle])
            else:
                blog_list2.append([blog_name, blog_image,
                                   blog_url, blog_subtitle])
            vals = {
                'blogs1': blog_list1,
                'blogs2': blog_list2
            }
        response = http.Response(
            template='website_snippet.website_snippet_view',
            qcontext=vals)
        return response.render()
