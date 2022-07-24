import tableauserverclient as TSC

def dashboard_views(workbookname,tableau_auth,server):
    """
    Takes in a workbook name and gives back the populated views.
    Arguements: 
    workbookname  - string
        The name of the workbook to be matched
    tableau_auth - string
        Authentication for the session
    server - string
        Server instance for the session
    """
    req_option = TSC.RequestOptions()
    req_option.filter.add(TSC.Filter(TSC.RequestOptions.Field.Name,
                                TSC.RequestOptions.Operator.Equals,
                                workbookname))
    matching_workbooks, pagination_item = server.workbooks.get(req_option)
    wbmatch = matching_workbooks[0]
    server.workbooks.get_by_id(wbmatch.id)
    server.workbooks.populate_views(wbmatch,usage=True)
    output = [view for view in wbmatch.views]
    return output