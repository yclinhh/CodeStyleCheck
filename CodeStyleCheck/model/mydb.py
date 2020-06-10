#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time : 2020/4/28 19:01
# @Author : yachao_lin
# @File : mydb.py

import pymysql


class MysqlOperation:
    # 初始化一个数据库连接实例
    def __init__(self, host, user, pwd, database):
        self.host = host
        self.user = user
        self.pwd = pwd
        self.database = database
        self.db = None
        self.cursor = None

    def connect(self):
        """
        连接数据库
        :return: None
        """
        try:
            self.db = pymysql.connect(self.host, self.user, self.pwd, self.database)
            self.cursor = self.db.cursor()
            print("数据库连接成功!")
        except Exception as e:
            print(e)
            print("数据库连接失败!")

    # 关闭数据库
    def close(self):
        self.cursor.close()
        self.db.close()

    def select_one(self, sql):
        """
        查询一条数据
        :param sql:
        :return: 以元组形式返回信息
        """
        res = None
        try:
            self.connect()
            self.cursor.execute(sql)
            res = self.cursor.fetchone()
            self.close()
            print("查询一条数据成功!")
            # print("res", res)
        except Exception as e:
            print(e)
            print("查询一条数据失败!")
        return res

    def select_all(self, sql):
        """
        查询多条数据
        :param sql:
        :return: 元组
        """
        res = None
        descr = None
        try:
            self.connect()
            self.cursor.execute(sql)
            res = self.cursor.fetchall()
            descr = self.cursor.description
            self.close()
            print("查询所有数据成功!")
        except Exception as e:
            print(e)
            print("查询所有数据失败!")
        finally:
            return res, descr

    # 插入数据
    def insert(self, sql):
        return self.__edit(sql)

    # 更新数据
    def update(self, sql):
        return self.__edit(sql)

    # 删除数据
    def delete(self, sql):
        return self.__edit(sql)

    def __edit(self, sql):
        """
        函数名双下划线开头---->封装此函数为类的私有方法
        :param sql:
        :return: 受影响的行
        """
        count = 0
        try:
            self.connect()
            try:
                count = self.cursor.execute(sql)
                self.db.commit()
                self.close()
                print("提交成功!")
            except Exception as e:
                print(e)
                print("提交失败!")
        except Exception as e1:
            print(e1)
            print("连接数据库失败!")
            self.db.rollback()
        finally:
            return count


if __name__ == "__main__":
    s = MysqlOperation("localhost", "root", "123456", "cstyle_db")
    sqll = "select * from error"
    s.connect()
    s1 = s.select_one(sqll)
    s2 = s.select_all(sqll)
    print(s1)
    print(s2)
