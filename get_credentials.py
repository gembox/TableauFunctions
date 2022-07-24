def get_site_credentials():
    """
    This function reads files and passes back credentials for sign in.
    Returns: user,token,site
    """
    with open('C:\\creds\\pat.txt', 'r') as file :
        token = file.read()

    with open('C:\\creds\\name.txt', 'r') as file :
        user = file.read()

    with open('C:\\creds\\site.txt', 'r') as file :
        site = file.read()

    return(user,token,site)