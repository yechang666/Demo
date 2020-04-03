import unittest
import HtmlTestRunner


class MyTestCase(unittest.TestCase):
    def tearDown(self):
        print('1111')
    def setUp(self):
        print("2222")
    @classmethod
    def tearDownClass(self):
        print(44444)
    @classmethod
    def setUpClass(self):
        print("33333" + "\n")

    def test_something(self):
        self.assertEqual(True, True)
    def test_um(self):
        print("who i am")

    def test_run(self):
        # self.assertEqual(1,1)
        self.assertIs(1, 1)
        # 测试用例

    def test_run2(self):
        # self.assertEqual(1,1)
        self.assertIs(1, 1)
        # 测试用例

    def test_run3(self):
        # self.assertEqual(1,1)
        self.assertIs(1, 1)
        # 测试用例

    def test_run1(self):
        # self.assertEqual(1,1)
        self.assertIs(1, 1)
        # 测试用例


if __name__ == '__main__':
    # unittest.main()
    test_suite = unittest.TestSuite()
    # test_suite.addTest(MyTestCase('test_um'))#添加测试用例
    test_suite.addTest(unittest.makeSuite(MyTestCase))
    fp = open('res.html','wb')
    runner = HtmlTestRunner.HTMLTestRunner(stream=fp,report_title="api报告",descriptions="测试情况")
    runner.run(test_suite)