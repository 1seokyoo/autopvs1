from flask_restplus import Api
from flask import url_for
from .autopvs1_endpoints import api as ns_pvs1

# Override standard specs_url to allow reverse-proxy access through mod_wsgi
class CustomAPI(Api):
    @property
    def specs_url(self):
        """
        The Swagger specifications absolute url (ie. `swagger.json`)

        This method returns the path relative to the APP required for reverse proxy access

        :rtype: str
        """
        return url_for(self.endpoint('specs'), _external=False)


# Define the API as api
api = CustomAPI(version='0.1',
                title="rest_AutoPVS1",
                description=""
          )

# Add the namespaces to the API
api.add_namespace(ns_pvs1)