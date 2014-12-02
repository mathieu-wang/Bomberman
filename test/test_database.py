import unittest
from database import Database

class TestDatabase(unittest.TestCase):
    TestRealName = "Test User"
    TestValidUsername1 = "testUser1"
    TestValidUsername2 = "testUser2"
    TestValidRealname = "testRealName"
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

    def testCreateUser(self):
        self.assertFalse(self.db.hasUser(TestDatabase.TestValidUsername1))
        self.createTestUser1()
        self.assertTrue(self.db.hasUser(TestDatabase.TestValidUsername1))

    def testUpdateUserAccountWithExistingUsername(self):
        self.createTestUser1()
        self.createTestUser2()
        self.assertFalse(self.db.updateUserAccount(TestDatabase.TestValidUsername1, TestDatabase.TestValidUsername2, TestDatabase.TestValidRealname, TestDatabase.TestValidPassword))

    def testUpdateUserAccountWithValidCredentials(self):
        self.createTestUser1()
        self.assertFalse(self.db.hasUser(TestDatabase.TestValidUsername2))
        self.assertTrue(self.db.updateUserAccount(TestDatabase.TestValidUsername1, TestDatabase.TestValidUsername2, TestDatabase.TestValidRealname, TestDatabase.TestValidPassword))
        self.assertTrue(self.db.hasUser(TestDatabase.TestValidUsername2))

    def testIsValidUsername(self):
        self.assertTrue(self.db.isValidUsername(TestDatabase.TestValidUsername1))
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

        self.createTestUser1()
        self.assertEqual(self.db.getHighestUnlockedLevel(TestDatabase.TestValidUsername1), 1)

    def testUpdateUserScore(self):
        self.db.createUserAccountsForDemo()
        self.assertEqual(self.db.getUserAccount("Demo05")['cumulativeScore'], 16000)
        self.db.updateUserScore("Demo05", 0)
        self.assertEqual(self.db.getUserAccount("Demo05")['cumulativeScore'], 16000)
        self.db.updateUserScore("Demo05", 1000)
        self.assertEqual(self.db.getUserAccount("Demo05")['cumulativeScore'], 17000)

    def testUpdateNumGamesPlayed(self):
        self.createTestUser1()
        self.assertEqual(self.db.getUserAccount(TestDatabase.TestValidUsername1)['numGamesPlayed'], 0)
        self.db.incrementNumOfGamesPlayed(TestDatabase.TestValidUsername1)
        self.assertEqual(self.db.getUserAccount(TestDatabase.TestValidUsername1)['numGamesPlayed'], 1)

    def createTestUser1(self):
        self.db.createUser(TestDatabase.TestRealName, TestDatabase.TestValidUsername1, TestDatabase.TestInvalidPasswordNoSpecial)

    def createTestUser2(self):
        self.db.createUser(TestDatabase.TestRealName, TestDatabase.TestValidUsername2, TestDatabase.TestInvalidPasswordNoSpecial)


if __name__ == '__main__':

    unittest.main()
