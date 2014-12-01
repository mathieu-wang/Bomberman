import unittest
from database import Database

class TestDatabase(unittest.TestCase):
    TestRealName = "Test User"
    TestValidUsername = "testUser"
    TestInvalidUsernameEmpty = ""
    TestInvalidUsernameTooShort = "user1"
    TestValidPassword = "testPassword$0"
    TestInvalidPasswordTooShort = "De@1"
    TestInvalidPasswordNoSpecial = "testPassword0"
    TestInvalidPasswordNoDigit = "testPassword$"
    TestInvalidPasswordNoUpper = "testpassword$0"
    TestInvalidPasswordNoLower = "TESTPASSWORD$0"

    def setUp(self):
        self.db = Database(True)

    def tearDown(self):
        pass

    def testCreateUser(self):
        self.assertFalse(self.db.hasUser(TestDatabase.TestValidUsername))
        self.createTestUser()
        self.assertTrue(self.db.hasUser(TestDatabase.TestValidUsername))

    def testIsValidUsername(self):
        self.assertTrue(self.db.isValidUsername(TestDatabase.TestValidUsername))
        self.assertFalse(self.db.isValidUsername(TestDatabase.TestInvalidUsernameEmpty))
        self.assertFalse(self.db.isValidUsername(TestDatabase.TestInvalidUsernameTooShort))

    def testIsValidPassword(self):
        self.assertTrue(self.db.isValidPassword(TestDatabase.TestValidPassword))
        self.assertFalse(self.db.isValidPassword(TestDatabase.TestInvalidPasswordTooShort))
        self.assertFalse(self.db.isValidPassword(TestDatabase.TestInvalidPasswordNoSpecial))
        self.assertFalse(self.db.isValidPassword(TestDatabase.TestInvalidPasswordNoDigit))
        self.assertFalse(self.db.isValidPassword(TestDatabase.TestInvalidPasswordNoLower))
        self.assertFalse(self.db.isValidPassword(TestDatabase.TestInvalidPasswordNoUpper))

    def testGetTopTenUsers(self):
        self.db.createUserAccountsForDemo()
        users = self.db.getTopTenUsers()

        iter = users.__iter__()
        self.assertEqual(iter.__next__()['username'], "Demo05")
        self.assertEqual(iter.__next__()['username'], "Demo06")
        self.assertEqual(iter.__next__()['username'], "Demo07")
        self.assertEqual(iter.__next__()['username'], "Demo04")
        self.assertEqual(iter.__next__()['username'], "Demo03")
        self.assertEqual(iter.__next__()['username'], "Demo10")
        self.assertEqual(iter.__next__()['username'], "Demo09")
        self.assertEqual(iter.__next__()['username'], "Demo01")
        self.assertEqual(iter.__next__()['username'], "Demo02")
        self.assertEqual(iter.__next__()['username'], "Demo08")

    def testGetHighestUnlockedLevel(self):
        self.db.createUserAccountsForDemo()
        self.assertEqual(self.db.getHighestUnlockedLevel("Demo01"), 11)
        self.assertEqual(self.db.getHighestUnlockedLevel("Demo05"), 15)

        self.createTestUser()
        self.assertEqual(self.db.getHighestUnlockedLevel(TestDatabase.TestValidUsername), 1)

    def testUpdateUserScore(self):
        self.db.createUserAccountsForDemo()
        self.assertEqual(self.db.getUserAccount("Demo05")['cumulativeScore'], 16000)
        self.db.updateUserScore("Demo05", 0)
        self.assertEqual(self.db.getUserAccount("Demo05")['cumulativeScore'], 16000)
        self.db.updateUserScore("Demo05", 1000)
        self.assertEqual(self.db.getUserAccount("Demo05")['cumulativeScore'], 17000)

    def testUpdateNumGamesPlayed(self):
        self.createTestUser()
        self.assertEqual(self.db.getUserAccount(TestDatabase.TestValidUsername)['numGamesPlayed'], 0)
        self.db.incrementNumOfGamesPlayed(TestDatabase.TestValidUsername)
        self.assertEqual(self.db.getUserAccount(TestDatabase.TestValidUsername)['numGamesPlayed'], 1)



    def createTestUser(self):
        self.db.createUser(TestDatabase.TestRealName, TestDatabase.TestValidUsername, TestDatabase.TestInvalidPasswordNoSpecial)


if __name__ == '__main__':

    unittest.main()
