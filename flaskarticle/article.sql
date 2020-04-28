DROP TABLE IF EXISTS tb_master;
DROP TABLE IF EXISTS tb_article;
DROP TABLE IF EXISTS tb_masterfriend;
DROP TABLE IF EXISTS tb_articleread;
DROP TABLE IF EXISTS tb_articlepraise;
DROP TABLE IF EXISTS tb_articlecollect;
DROP TABLE IF EXISTS tb_articleshare;

--博主表
CREATE TABLE tb_master (
  masterid INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  mastertime TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  mastername TEXT,
  mastersex CHAR(2) default '男' CHECK (mastersex in('男','女')),
  masterphone TEXT,
  masteremail TEXT,
  masterwechat TEXT,
  masterqq TEXT
);

--文章表
CREATE TABLE tb_article (
  articleid INTEGER PRIMARY KEY AUTOINCREMENT,
  master_id INTEGER NOT NULL,
  articletime TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  articletitle TEXT NOT NULL,
  articlecontent TEXT NOT NULL,
  articlefrom TEXT NOT NULL,
  articletype CHAR(10) default '0' CHECK (articletype in('0','1','2','3','4','5','6','7','8','9')),
  articleread INTEGER,
  articlepraise INTEGER,
  articlecollect INTEGER,
  articleshare INTEGER,
  FOREIGN KEY (master_id) REFERENCES tb_master (masterid)
);

--博主好友表
CREATE TABLE tb_masterfriend (
  masterfriendid INTEGER PRIMARY KEY AUTOINCREMENT,
  masterfriendtime TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  master_id INTEGER NOT NULL,--博主id
  masterfriend_id INTEGER NOT NULL,--粉丝id
  masterfriendtype CHAR(2) default '粉丝' CHECK (masterfriendtype in('粉丝','好友')),
  FOREIGN KEY (master_id) REFERENCES tb_master (masterid),
  FOREIGN KEY (masterfriend_id) REFERENCES tb_master (masterid)
);

-- 文章阅读表
CREATE TABLE tb_articleread (
  articlereadid INTEGER PRIMARY KEY AUTOINCREMENT,
  articlereadtime TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  article_id INTEGER NOT NULL,--文章id
  articleread_id INTEGER NOT NULL,--阅读者id
  FOREIGN KEY (article_id) REFERENCES tb_article (articleid),
  FOREIGN KEY (articleread_id) REFERENCES tb_master (masterid)
);

-- 文章点赞表
CREATE TABLE tb_articlepraise (
  articlepraiseid INTEGER PRIMARY KEY AUTOINCREMENT,
  articlepraisetime TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  article_id INTEGER NOT NULL,--文章id
  articlepraise_id INTEGER NOT NULL,--点赞者id
  FOREIGN KEY (article_id) REFERENCES tb_article (articleid),
  FOREIGN KEY (articlepraise_id) REFERENCES tb_master (masterid)
);

-- 文章收藏表
CREATE TABLE tb_articlecollect (
  articlecollectid INTEGER PRIMARY KEY AUTOINCREMENT,
  articlecollecttime TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  article_id INTEGER NOT NULL,--文章id
  articlecollect_id INTEGER NOT NULL,--收藏者id
  FOREIGN KEY (article_id) REFERENCES tb_article (articleid),
  FOREIGN KEY (articlecollect_id) REFERENCES tb_master (masterid)
);

-- 文章分享表
CREATE TABLE tb_articleshare (
  articleshareid INTEGER PRIMARY KEY AUTOINCREMENT,
  articlesharetime TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  article_id INTEGER NOT NULL,--文章id
  articleshare_id INTEGER NOT NULL,--分享者id
  FOREIGN KEY (article_id) REFERENCES tb_article (articleid),
  FOREIGN KEY (articleshare_id) REFERENCES tb_master (masterid)
);