#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File: test.py
# Author: alukard <alukard@github>
# Date: 05.02.2021

import unittest

try: 
    from PayLoad import PayLoad
except:
    pass

try:
    from Reddit import Reddit
except:
    pass

class TestPayLoad(unittest.TestCase):

    def test_init(self):
        self.p = PayLoad()


    def test_append(self):
        self.test_init()

        p = self.p
        self.assertEqual(p, [])
        p.append( "example", "no")

        self.assertEqual( p[-1], p[0])
        self.assertEqual( p[-1].post, "example")
        self.assertEqual( p[-1].meta, "no")

        p.append( "example2", "yes")

        self.assertNotEqual( p[-1], p[0])
        self.assertEqual( p[0].post, "example")
        self.assertEqual( p[0].meta, "no")
        self.assertEqual( p[-1].post, "example2")
        self.assertEqual( p[-1].meta, "yes")


    def test_tuple(self):
        self.test_append()
        p = self.p

        self.assertEqual( p[0][0], p[0].time)
        self.assertEqual( p[1][2], p[1].meta)


    def __test_readwrite(self):
        self.test_append()
        p = self.p 


        p.write()

        p = PayLoad()

        self.assertEqual( p, self.p )



class TestReddit(unittest.TestCase):

    def dec_iter(func):
        def wrapper (self):
            self.test_init()

            n = 10
            for post in self.r:
                func(self, post)
                #self.r.PayLoad.append(post)
                n -= 1 
                if (0 == n): return 

        return wrapper


    def test_init(self):
        self.r = Reddit("bot4")



    @dec_iter
    def test_iter(     self, post):
        pass

    @dec_iter 
    def __test_iterprint(self, post):
        print ( post )


    def test_upvote(self):
        self.test_init()

        print ( "event loop active")
        self.r.updown()

        print( self.r.PayLoad)
    



    def test_payload(self):
        self.test_iter()

        for pay in self.r.PayLoad:
            pass




if __name__ == '__main__':
    unittest.main()

