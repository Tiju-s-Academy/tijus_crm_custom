from odoo import models,fields,api
from odoo.osv import expression


class MailMessage(models.Model):
    _inherit = "mail.message"
    _order = "create_date desc"

class MailMessage(models.Model):
    _inherit = 'mail.message'

    # Override
    @api.model
    def _message_fetch(self, domain, search_term=None, before=None, after=None, around=None, limit=30):
        res = {}
        if search_term:
            # Replace spaces with '%' for broader matching in search terms
            search_term = search_term.replace(" ", "%")
            domain = expression.AND([domain, expression.OR([
                # Access to attachments is allowed if you have access to the parent model
                [("attachment_ids", "in", self.env["ir.attachment"].sudo()._search([("name", "ilike", search_term)]))],
                [("body", "ilike", search_term)],
                [("subject", "ilike", search_term)],
                [("subtype_id.description", "ilike", search_term)],
            ])])
            domain = expression.AND([domain, [("message_type", "not in", ["user_notification", "notification"])]])
            res["count"] = self.search_count(domain)

        if around:
            messages_before = self.search(
                domain=[*domain, ('create_date', '<=', around)], 
                limit=limit // 2, 
                order="create_date DESC"
            )
            messages_after = self.search(
                domain=[*domain, ('create_date', '>', around)], 
                limit=limit // 2, 
                order='create_date ASC'
            )
            # Merge and sort messages by create_date in descending order (most recent first)
            return {**res, "messages": (messages_after + messages_before).sorted('create_date', reverse=True)}

        if before:
            domain = expression.AND([domain, [('create_date', '<', before)]])
        if after:
            domain = expression.AND([domain, [('create_date', '>', after)]])

        res["messages"] = self.search(
            domain, 
            limit=limit, 
            order='create_date ASC' if after else 'create_date DESC'
        )

        if after:
            # Reverse sorting to maintain the correct order after fetching
            res["messages"] = res["messages"].sorted('create_date', reverse=True)
        
        return res
