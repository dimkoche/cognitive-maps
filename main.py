import web

urls = (
    '/', 'views.view.Index',
    '/about', 'views.view.About',
    '/map/new', 'views.view.MapAdd',
    '/map/show/(.+)', 'views.view.MapShow',
    '/map/add-factor', 'views.view.MapAddFactor',
    '/map/change-factor', 'views.view.MapChangeFactor',
    '/map/update-image', 'views.view.MapUpdateImage',
    '/map/change-koef', 'views.view.MapChangeKoef',
    '/map/get-chart-data', 'views.view.MapGetChartData',
)

if __name__ == "__main__":
    app = web.application(urls, globals())
    app.internalerror = web.debugerror

    session = web.session.Session(
        app,
        web.session.DiskStore('sessions'),
        initializer={'user_id': 0, 'username': 'Guest'}
    )
    web.web_session = session

    app.run()
