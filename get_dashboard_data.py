import csv
import tableauserverclient as TSC
from get_views_from_dashboard import dashboard_views
from get_credentials import get_site_credentials

creds = get_site_credentials()

tableau_auth = TSC.PersonalAccessTokenAuth(creds[0],creds[1],creds[2])
server = TSC.Server('https://10ax.online.tableau.com', use_server_version=True)

with server.auth.sign_in(tableau_auth):
    mviews = dashboard_views('ProductWorkbook',tableau_auth,server)
    for view in mviews:
        if view.name != 'Product':
            server.views.populate_csv(view)
            with open('{}.csv'.format(view.name), 'wb') as f:
                # Perform byte join on the CSV data
                f.write(b''.join(view.csv))
        else:
            print('No data output written for view named {}'.format(view.name))
        
            