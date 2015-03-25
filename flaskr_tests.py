import os
import flaskr
import unittest
import tempfile

class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, flaskr.app.config['DATABASE'] = tempfile.mkstemp()
        flaskr.app.config['TESTING'] = True
        self.app = flaskr.app.test_client()
        flaskr.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink( flaskr.app.config['DATABASE'] )

    def test_empty_db(self):
        rv = self.app.get('/')
        assert 'No entries here yet' in rv.data

    def login(self, username, password):
        return self.app.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)

    def test_multiple_login_logout(self):
        # Test admin login

        # for key in flaskr.USERS:
        #     rv = self.login(key,flaskr.USERS[key])
        #     assert 'You were logged in' in rv.data
        #     rv = self.logout()
        #     assert 'You were logged out' in rv.data

        rv = self.login('admin', 'default')
        assert 'You were logged in' in rv.data
        rv = self.logout()
        assert 'You were logged out' in rv.data

        # Test Jim login
        rv = self.login('jim', 'bean')
        assert 'You were logged in' in rv.data
        rv = self.logout()
        assert 'You were logged out' in rv.data

        # Test Spock login
        rv = self.login('spock', 'vulcan')
        assert 'You were logged in' in rv.data
        rv = self.logout()
        assert 'You were logged out' in rv.data


        # Test non-recognised users
        rv = self.login('adminx', 'default')
        assert 'Invalid username' in rv.data
        rv = self.login('admin', 'defaultx')
        assert 'Invalid password' in rv.data

    def test_login_logout(self):
        rv = self.login('admin', 'default')
        assert 'You were logged in' in rv.data
        rv = self.logout()
        assert 'You were logged out' in rv.data
        rv = self.login('adminx', 'default')
        assert 'Invalid username' in rv.data
        rv = self.login('admin', 'defaultx')
        assert 'Invalid password' in rv.data

    def test_messages(self):
        self.login('admin', 'default')
        rv = self.app.post('/add', data=dict(
            title='<Hello>',
            text='<strong>HTML</strong> allowed here',
            start_time='',
            end_time=''
        ), follow_redirects=True)
        assert 'No entries here so far' not in rv.data
        assert '&lt;Hello&gt;' in rv.data
        assert '<strong>HTML</strong> allowed here' in rv.data

    def test_by_someone(self):
        self.login('admin', 'default')
        rv = self.app.post('/add', data=dict(
            title='<Hello>',
            text='<strong>HTML</strong> allowed here',
            start_time='<22:00>',
            end_time='<23:00>'
        ), follow_redirects=True)
        # assert 'by admin'
        assert 'by admin' in rv.data


    def test_time (self):
        self.login('admin', 'default')
        rv = self.app.post('/add', data=dict(
            title='<Hello>',
            text='<strong>HTML</strong> allowed here',
            start_time='<22:00>',
            end_time='<23:00>'
        ), follow_redirects=True)
        # assert 'time'
        assert 'by admin' in rv.data
        assert '&lt;22:00&gt; &lt;23:00&gt;' in rv.data






if __name__ == '__main__':
    unittest.main()

