/*
 Navicat Premium Data Transfer

 Source Server         : database
 Source Server Type    : SQLite
 Source Server Version : 3030001
 Source Schema         : main

 Target Server Type    : SQLite
 Target Server Version : 3030001
 File Encoding         : 65001

 Date: 28/07/2022 12:56:03
*/

PRAGMA foreign_keys = false;

-- ----------------------------
-- Table structure for alembic_version
-- ----------------------------
DROP TABLE IF EXISTS "alembic_version";
CREATE TABLE "alembic_version" (
  "version_num" VARCHAR(32) NOT NULL,
  CONSTRAINT "alembic_version_pkc" PRIMARY KEY ("version_num")
);

-- ----------------------------
-- Records of alembic_version
-- ----------------------------
INSERT INTO "alembic_version" VALUES ('16decb353962');

-- ----------------------------
-- Table structure for cp_dept
-- ----------------------------
DROP TABLE IF EXISTS "cp_dept";
CREATE TABLE "cp_dept" (
  "id" INTEGER NOT NULL,
  "parent_id" INTEGER,
  "dept_name" VARCHAR(50),
  "leader" VARCHAR(50),
  "phone" VARCHAR(20),
  "email" VARCHAR(50),
  "status" BOOLEAN,
  "comment" TEXT,
  "address" VARCHAR(255),
  "sort" INTEGER,
  "create_at" DATETIME,
  PRIMARY KEY ("id")
);

-- ----------------------------
-- Records of cp_dept
-- ----------------------------
INSERT INTO "cp_dept" VALUES (1, 0, '总公司', '就眠仪式', 12312345679, '123qq.com', 1, NULL, '这是总公司', 1, '2022-07-25 11:37:49.388744');
INSERT INTO "cp_dept" VALUES (4, 1, '济南分公司', '就眠仪式', 12312345678, '1234qq.com', 1, NULL, '这是济南', 2, '2021-06-01 17:24:33.000000');
INSERT INTO "cp_dept" VALUES (5, 1, '唐山分公司', 'mkg', 12312345678, '123@qq.com', 1, NULL, '这是唐山', 4, '2021-06-01 17:25:15.000000');
INSERT INTO "cp_dept" VALUES (7, 4, '济南分公司开发部', '就眠仪式', 12312345678, '123@qq.com', 1, NULL, '测试', 5, '2021-06-01 17:27:39.000000');
INSERT INTO "cp_dept" VALUES (8, 5, '唐山测试部', 'mkg', 12312345678, '123@qq.com', 1, NULL, '测试部', 6, '2021-06-01 17:28:27.000000');

-- ----------------------------
-- Table structure for cp_user
-- ----------------------------
DROP TABLE IF EXISTS "cp_user";
CREATE TABLE "cp_user" (
  "id" INTEGER NOT NULL,
  "username" VARCHAR(20),
  "realname" VARCHAR(20),
  "mobile" VARCHAR(11),
  "avatar" VARCHAR(255),
  "comment" VARCHAR(255),
  "password_hash" VARCHAR(128),
  "enable" INTEGER,
  "dept_id" INTEGER,
  "create_at" DATETIME,
  "update_at" DATETIME,
  PRIMARY KEY ("id")
);

-- ----------------------------
-- Records of cp_user
-- ----------------------------
INSERT INTO "cp_user" VALUES (1, 'admin', '超级管理', NULL, 'http://127.0.0.1:5000/_uploads/photos/1617291580000.jpg', NULL, 'pbkdf2:sha256:150000$raM7mDSr$58fe069c3eac01531fc8af85e6fc200655dd2588090530084d182e6ec9d52c85', 1, 1, '2022-07-25 11:37:49.405578', '2021-06-01 17:28:55.000000');

-- ----------------------------
-- Table structure for file_photo
-- ----------------------------
DROP TABLE IF EXISTS "file_photo";
CREATE TABLE "file_photo" (
  "id" INTEGER NOT NULL,
  "name" VARCHAR(255) NOT NULL,
  "href" VARCHAR(255),
  "mime" CHAR(50) NOT NULL,
  "size" CHAR(30) NOT NULL,
  "create_at" DATETIME,
  "update_at" DATETIME,
  PRIMARY KEY ("id")
);

-- ----------------------------
-- Records of file_photo
-- ----------------------------
INSERT INTO "file_photo" VALUES (3, '6958819_pear-admin_1607443454_1.png', 'http://127.0.0.1:5000/_uploads/photos/6958819_pear-admin_1607443454_1.png', 'image/png', 2204, '2022-07-25 11:37:49.392362', '2022-07-25 11:37:49.392368');
INSERT INTO "file_photo" VALUES (17, '1617291580000.jpg', 'http://127.0.0.1:5000/_uploads/photos/1617291580000.jpg', 'image/png', 94211, '2022-07-25 11:37:49.392369', '2022-07-25 11:37:49.392370');

-- ----------------------------
-- Table structure for lg_logging
-- ----------------------------
DROP TABLE IF EXISTS "lg_logging";
CREATE TABLE "lg_logging" (
  "id" INTEGER NOT NULL,
  "method" VARCHAR(10),
  "uid" INTEGER,
  "url" VARCHAR(255),
  "desc" TEXT,
  "ip" VARCHAR(255),
  "success" BOOLEAN,
  "user_agent" TEXT,
  "create_at" DATETIME,
  "update_at" DATETIME,
  PRIMARY KEY ("id")
);

-- ----------------------------
-- Records of lg_logging
-- ----------------------------
INSERT INTO "lg_logging" VALUES (1, 'POST', 1, '/api/v1/passport/login', '{''password'': ''123456'', ''captcha'': ''4302'', ''username'': ''admin''}', '127.0.0.1', 1, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.66 Safari/537.36 Edg/103.0.1264.44', '2022-07-25 11:38:31.186518', '2022-07-25 11:38:31.186527');
INSERT INTO "lg_logging" VALUES (2, 'GET', 1, '/users/', '{}', '127.0.0.1', 1, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.66 Safari/537.36 Edg/103.0.1264.44', '2022-07-25 11:38:37.699013', '2022-07-25 11:38:37.699019');
INSERT INTO "lg_logging" VALUES (3, 'GET', 1, '/file', '{}', '127.0.0.1', 1, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.66 Safari/537.36 Edg/103.0.1264.44', '2022-07-25 11:38:39.725130', '2022-07-25 11:38:39.725135');
INSERT INTO "lg_logging" VALUES (4, 'POST', 1, '/api/v1/passport/login', '{''password'': ''123456'', ''captcha'': ''3414'', ''username'': ''admin''}', '127.0.0.1', 1, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.66 Safari/537.36 Edg/103.0.1264.44', '2022-07-27 20:23:48.052929', '2022-07-27 20:23:48.052939');
INSERT INTO "lg_logging" VALUES (5, 'GET', 1, '/rights/', '{}', '127.0.0.1', 1, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.66 Safari/537.36 Edg/103.0.1264.44', '2022-07-27 20:23:54.391269', '2022-07-27 20:23:54.391276');
INSERT INTO "lg_logging" VALUES (6, 'GET', 1, '/admin/role/', '{}', '127.0.0.1', 1, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.66 Safari/537.36 Edg/103.0.1264.44', '2022-07-27 20:23:56.871621', '2022-07-27 20:23:56.871627');
INSERT INTO "lg_logging" VALUES (7, 'GET', 1, '/dept', '{}', '127.0.0.1', 1, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.66 Safari/537.36 Edg/103.0.1264.44', '2022-07-27 20:23:58.613918', '2022-07-27 20:23:58.613924');
INSERT INTO "lg_logging" VALUES (8, 'GET', 1, '/users/', '{}', '127.0.0.1', 1, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.66 Safari/537.36 Edg/103.0.1264.44', '2022-07-27 20:24:01.362335', '2022-07-27 20:24:01.362341');
INSERT INTO "lg_logging" VALUES (9, 'GET', 1, '/users/', '{}', '127.0.0.1', 1, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.66 Safari/537.36 Edg/103.0.1264.44', '2022-07-27 20:25:00.689690', '2022-07-27 20:25:00.689696');
INSERT INTO "lg_logging" VALUES (10, 'GET', 1, '/rights/', '{}', '127.0.0.1', 1, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.66 Safari/537.36 Edg/103.0.1264.44', '2022-07-27 20:26:05.929319', '2022-07-27 20:26:05.929334');
INSERT INTO "lg_logging" VALUES (11, 'GET', 1, '/dept', '{}', '127.0.0.1', 1, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.66 Safari/537.36 Edg/103.0.1264.44', '2022-07-27 20:26:06.669248', '2022-07-27 20:26:06.669255');
INSERT INTO "lg_logging" VALUES (12, 'GET', 1, '/rights/power/18', '{}', '127.0.0.1', 1, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.66 Safari/537.36 Edg/103.0.1264.44', '2022-07-27 20:26:28.151429', '2022-07-27 20:26:28.151440');
INSERT INTO "lg_logging" VALUES (13, 'GET', 1, '/rights/', '{}', '127.0.0.1', 1, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.66 Safari/537.36 Edg/103.0.1264.44', '2022-07-27 20:26:50.623596', '2022-07-27 20:26:50.623602');
INSERT INTO "lg_logging" VALUES (14, 'GET', 1, '/dept', '{}', '127.0.0.1', 1, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.66 Safari/537.36 Edg/103.0.1264.44', '2022-07-27 20:26:50.624167', '2022-07-27 20:26:50.624172');
INSERT INTO "lg_logging" VALUES (15, 'GET', 1, '/rights/add', '{}', '127.0.0.1', 1, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.66 Safari/537.36 Edg/103.0.1264.44', '2022-07-27 20:27:02.609873', '2022-07-27 20:27:02.609878');
INSERT INTO "lg_logging" VALUES (16, 'GET', 1, '/rights/power/1', '{}', '127.0.0.1', 1, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.66 Safari/537.36 Edg/103.0.1264.44', '2022-07-27 20:27:12.661805', '2022-07-27 20:27:12.661812');
INSERT INTO "lg_logging" VALUES (17, 'GET', 1, '/rights/add', '{}', '127.0.0.1', 1, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.66 Safari/537.36 Edg/103.0.1264.44', '2022-07-27 20:27:15.880640', '2022-07-27 20:27:15.880647');
INSERT INTO "lg_logging" VALUES (18, 'GET', 1, '/rights/', '{}', '127.0.0.1', 1, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.66 Safari/537.36 Edg/103.0.1264.44', '2022-07-27 20:27:48.558477', '2022-07-27 20:27:48.558488');
INSERT INTO "lg_logging" VALUES (19, 'GET', 1, '/rights/', '{}', '127.0.0.1', 1, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.66 Safari/537.36 Edg/103.0.1264.44', '2022-07-27 20:29:06.759753', '2022-07-27 20:29:06.759761');
INSERT INTO "lg_logging" VALUES (20, 'GET', 1, '/rights/', '{}', '127.0.0.1', 1, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.66 Safari/537.36 Edg/103.0.1264.44', '2022-07-27 20:29:57.735011', '2022-07-27 20:29:57.735018');
INSERT INTO "lg_logging" VALUES (21, 'GET', 1, '/rights/', '{}', '127.0.0.1', 1, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.66 Safari/537.36 Edg/103.0.1264.44', '2022-07-27 20:30:01.920543', '2022-07-27 20:30:01.920550');
INSERT INTO "lg_logging" VALUES (22, 'GET', 1, '/rights/', '{}', '127.0.0.1', 1, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.66 Safari/537.36 Edg/103.0.1264.44', '2022-07-27 20:30:07.553127', '2022-07-27 20:30:07.553148');
INSERT INTO "lg_logging" VALUES (23, 'GET', 1, '/rights/', '{}', '127.0.0.1', 1, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.66 Safari/537.36 Edg/103.0.1264.44', '2022-07-27 20:30:08.897170', '2022-07-27 20:30:08.897176');
INSERT INTO "lg_logging" VALUES (24, 'GET', 1, '/rights/add', '{}', '127.0.0.1', 1, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.66 Safari/537.36 Edg/103.0.1264.44', '2022-07-27 20:30:14.606953', '2022-07-27 20:30:14.606960');
INSERT INTO "lg_logging" VALUES (25, 'GET', 1, '/rights/power/52', '{}', '127.0.0.1', 1, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.66 Safari/537.36 Edg/103.0.1264.44', '2022-07-27 20:30:20.026862', '2022-07-27 20:30:20.026868');
INSERT INTO "lg_logging" VALUES (26, 'GET', 1, '/rights/power/17', '{}', '127.0.0.1', 1, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.66 Safari/537.36 Edg/103.0.1264.44', '2022-07-27 20:30:25.727425', '2022-07-27 20:30:25.727432');
INSERT INTO "lg_logging" VALUES (27, 'GET', 1, '/rights/power/1', '{}', '127.0.0.1', 1, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.66 Safari/537.36 Edg/103.0.1264.44', '2022-07-27 20:30:29.250844', '2022-07-27 20:30:29.250852');
INSERT INTO "lg_logging" VALUES (28, 'GET', 1, '/rights/power/17', '{}', '127.0.0.1', 1, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.66 Safari/537.36 Edg/103.0.1264.44', '2022-07-27 20:30:34.939670', '2022-07-27 20:30:34.939676');
INSERT INTO "lg_logging" VALUES (29, 'GET', 1, '/rights/', '{}', '127.0.0.1', 1, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.66 Safari/537.36 Edg/103.0.1264.44', '2022-07-27 20:30:41.431916', '2022-07-27 20:30:41.431929');
INSERT INTO "lg_logging" VALUES (30, 'GET', 1, '/rights/', '{}', '127.0.0.1', 1, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.66 Safari/537.36 Edg/103.0.1264.44', '2022-07-27 20:30:42.524675', '2022-07-27 20:30:42.524682');
INSERT INTO "lg_logging" VALUES (31, 'GET', 1, '/rights/add', '{}', '127.0.0.1', 1, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.66 Safari/537.36 Edg/103.0.1264.44', '2022-07-27 20:30:44.273244', '2022-07-27 20:30:44.273251');
INSERT INTO "lg_logging" VALUES (32, 'GET', 1, '/rights/power/3', '{}', '127.0.0.1', 1, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.66 Safari/537.36 Edg/103.0.1264.44', '2022-07-27 20:30:51.833926', '2022-07-27 20:30:51.833933');
INSERT INTO "lg_logging" VALUES (33, 'GET', 1, '/rights/power/4', '{}', '127.0.0.1', 1, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.66 Safari/537.36 Edg/103.0.1264.44', '2022-07-27 20:30:54.976461', '2022-07-27 20:30:54.976467');
INSERT INTO "lg_logging" VALUES (34, 'GET', 1, '/rights/power/13', '{}', '127.0.0.1', 1, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.66 Safari/537.36 Edg/103.0.1264.44', '2022-07-27 20:30:57.403513', '2022-07-27 20:30:57.403519');
INSERT INTO "lg_logging" VALUES (35, 'GET', 1, '/rights/power/3', '{}', '127.0.0.1', 1, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.66 Safari/537.36 Edg/103.0.1264.44', '2022-07-27 20:31:01.359122', '2022-07-27 20:31:01.359129');
INSERT INTO "lg_logging" VALUES (36, 'GET', 1, '/rights/power/13', '{}', '127.0.0.1', 1, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.66 Safari/537.36 Edg/103.0.1264.44', '2022-07-27 20:31:04.515872', '2022-07-27 20:31:04.515879');
INSERT INTO "lg_logging" VALUES (37, 'GET', 1, '/rights/power/49', '{}', '127.0.0.1', 1, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.66 Safari/537.36 Edg/103.0.1264.44', '2022-07-27 20:31:08.175812', '2022-07-27 20:31:08.175819');
INSERT INTO "lg_logging" VALUES (38, 'GET', 1, '/rights/add', '{}', '127.0.0.1', 1, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.66 Safari/537.36 Edg/103.0.1264.44', '2022-07-27 20:31:12.799895', '2022-07-27 20:31:12.799901');
INSERT INTO "lg_logging" VALUES (39, 'GET', 1, '/rights/power/52', '{}', '127.0.0.1', 1, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.66 Safari/537.36 Edg/103.0.1264.44', '2022-07-27 20:31:21.991777', '2022-07-27 20:31:21.991784');
INSERT INTO "lg_logging" VALUES (40, 'GET', 1, '/rights/', '{}', '127.0.0.1', 1, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.66 Safari/537.36 Edg/103.0.1264.44', '2022-07-27 20:32:01.624929', '2022-07-27 20:32:01.624936');
INSERT INTO "lg_logging" VALUES (41, 'GET', 1, '/rights/', '{}', '127.0.0.1', 1, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.66 Safari/537.36 Edg/103.0.1264.44', '2022-07-27 20:32:07.358918', '2022-07-27 20:32:07.358925');
INSERT INTO "lg_logging" VALUES (42, 'GET', 1, '/rights/power/3', '{}', '127.0.0.1', 1, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.66 Safari/537.36 Edg/103.0.1264.44', '2022-07-27 20:32:21.806109', '2022-07-27 20:32:21.806116');
INSERT INTO "lg_logging" VALUES (43, 'GET', 1, '/rights/', '{}', '127.0.0.1', 1, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.66 Safari/537.36 Edg/103.0.1264.44', '2022-07-27 20:32:30.085099', '2022-07-27 20:32:30.085108');
INSERT INTO "lg_logging" VALUES (44, 'GET', 1, '/rights/', '{}', '127.0.0.1', 1, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.66 Safari/537.36 Edg/103.0.1264.44', '2022-07-27 20:32:50.582229', '2022-07-27 20:32:50.582236');
INSERT INTO "lg_logging" VALUES (45, 'GET', 1, '/dept', '{}', '127.0.0.1', 1, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.66 Safari/537.36 Edg/103.0.1264.44', '2022-07-27 20:32:53.632617', '2022-07-27 20:32:53.632623');
INSERT INTO "lg_logging" VALUES (46, 'GET', 1, '/users/', '{}', '127.0.0.1', 1, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.66 Safari/537.36 Edg/103.0.1264.44', '2022-07-27 20:32:59.676609', '2022-07-27 20:32:59.676616');
INSERT INTO "lg_logging" VALUES (47, 'GET', 1, '/rights/add', '{}', '127.0.0.1', 1, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.66 Safari/537.36 Edg/103.0.1264.44', '2022-07-27 20:34:30.780698', '2022-07-27 20:34:30.780706');
INSERT INTO "lg_logging" VALUES (48, 'GET', 1, '/rights/', '{}', '127.0.0.1', 1, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.66 Safari/537.36 Edg/103.0.1264.44', '2022-07-27 20:35:50.859907', '2022-07-27 20:35:50.859916');
INSERT INTO "lg_logging" VALUES (49, 'GET', 1, '/dept', '{}', '127.0.0.1', 1, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.66 Safari/537.36 Edg/103.0.1264.44', '2022-07-27 20:35:50.863505', '2022-07-27 20:35:50.863510');
INSERT INTO "lg_logging" VALUES (50, 'GET', 1, '/users/', '{}', '127.0.0.1', 1, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.66 Safari/537.36 Edg/103.0.1264.44', '2022-07-27 20:35:50.866598', '2022-07-27 20:35:50.866602');
INSERT INTO "lg_logging" VALUES (51, 'GET', 1, '/rights/power/52', '{}', '127.0.0.1', 1, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.66 Safari/537.36 Edg/103.0.1264.44', '2022-07-27 20:35:57.280311', '2022-07-27 20:35:57.280320');
INSERT INTO "lg_logging" VALUES (52, 'GET', 1, '/rights/power/53', '{}', '127.0.0.1', 1, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.66 Safari/537.36 Edg/103.0.1264.44', '2022-07-27 20:36:02.101996', '2022-07-27 20:36:02.102012');
INSERT INTO "lg_logging" VALUES (53, 'GET', 1, '/rights/', '{}', '127.0.0.1', 1, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.66 Safari/537.36 Edg/103.0.1264.44', '2022-07-27 20:36:05.221412', '2022-07-27 20:36:05.221423');
INSERT INTO "lg_logging" VALUES (54, 'GET', 1, '/rights/', '{}', '127.0.0.1', 1, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.66 Safari/537.36 Edg/103.0.1264.44', '2022-07-27 20:36:07.357591', '2022-07-27 20:36:07.357603');
INSERT INTO "lg_logging" VALUES (55, 'GET', 1, '/rights/power/52', '{}', '127.0.0.1', 1, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.66 Safari/537.36 Edg/103.0.1264.44', '2022-07-27 20:36:13.721398', '2022-07-27 20:36:13.721404');
INSERT INTO "lg_logging" VALUES (56, 'GET', 1, '/rights/power/52', '{}', '127.0.0.1', 1, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.66 Safari/537.36 Edg/103.0.1264.44', '2022-07-27 20:36:21.596880', '2022-07-27 20:36:21.596888');
INSERT INTO "lg_logging" VALUES (57, 'GET', 1, '/rights/power/53', '{}', '127.0.0.1', 1, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.66 Safari/537.36 Edg/103.0.1264.44', '2022-07-27 20:36:28.464525', '2022-07-27 20:36:28.464531');
INSERT INTO "lg_logging" VALUES (58, 'GET', 1, '/rights/', '{}', '127.0.0.1', 1, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.66 Safari/537.36 Edg/103.0.1264.44', '2022-07-27 20:50:37.834240', '2022-07-27 20:50:37.834254');
INSERT INTO "lg_logging" VALUES (59, 'GET', 1, '/admin/role/', '{}', '127.0.0.1', 1, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.66 Safari/537.36 Edg/103.0.1264.44', '2022-07-27 20:50:37.845136', '2022-07-27 20:50:37.845141');
INSERT INTO "lg_logging" VALUES (60, 'GET', 1, '/rights/power/52', '{}', '127.0.0.1', 1, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.66 Safari/537.36 Edg/103.0.1264.44', '2022-07-27 20:50:46.173244', '2022-07-27 20:50:46.173303');
INSERT INTO "lg_logging" VALUES (61, 'GET', 1, '/rights/power/4', '{}', '127.0.0.1', 1, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.66 Safari/537.36 Edg/103.0.1264.44', '2022-07-27 20:51:08.747344', '2022-07-27 20:51:08.747349');
INSERT INTO "lg_logging" VALUES (62, 'GET', 1, '/rights/power/52', '{}', '127.0.0.1', 1, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.66 Safari/537.36 Edg/103.0.1264.44', '2022-07-27 20:51:53.248263', '2022-07-27 20:51:53.248268');
INSERT INTO "lg_logging" VALUES (63, 'GET', 1, '/admin/role/power/1', '{}', '127.0.0.1', 1, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.66 Safari/537.36 Edg/103.0.1264.44', '2022-07-27 20:52:09.622020', '2022-07-27 20:52:09.622028');
INSERT INTO "lg_logging" VALUES (64, 'GET', 1, '/rights/', '{}', '127.0.0.1', 1, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.66 Safari/537.36 Edg/103.0.1264.44', '2022-07-27 20:52:14.674788', '2022-07-27 20:52:14.674797');
INSERT INTO "lg_logging" VALUES (65, 'GET', 1, '/admin/role/', '{}', '127.0.0.1', 1, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.66 Safari/537.36 Edg/103.0.1264.44', '2022-07-27 20:52:14.688316', '2022-07-27 20:52:14.688322');
INSERT INTO "lg_logging" VALUES (66, 'GET', 1, '/rights/', '{}', '127.0.0.1', 1, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.66 Safari/537.36 Edg/103.0.1264.44', '2022-07-27 20:52:47.023954', '2022-07-27 20:52:47.023962');
INSERT INTO "lg_logging" VALUES (67, 'GET', 1, '/rights/power/53', '{}', '127.0.0.1', 1, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.66 Safari/537.36 Edg/103.0.1264.44', '2022-07-27 20:52:57.187844', '2022-07-27 20:52:57.187850');
INSERT INTO "lg_logging" VALUES (68, 'POST', 1, '/api/v1/passport/login', '{''username'': ''admin'', ''captcha'': ''0443'', ''password'': ''123456''}', '127.0.0.1', 1, 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.66 Safari/537.36 Edg/103.0.1264.44', '2022-07-28 10:53:52.715480', '2022-07-28 10:53:52.715491');

-- ----------------------------
-- Table structure for pdscan_domain
-- ----------------------------
DROP TABLE IF EXISTS "pdscan_domain";
CREATE TABLE "pdscan_domain" (
  "id" INTEGER NOT NULL,
  "task_id" text NOT NULL,
  "domain" VARCHAR NOT NULL,
  "domain_record" VARCHAR NOT NULL,
  PRIMARY KEY ("id")
);

-- ----------------------------
-- Records of pdscan_domain
-- ----------------------------
INSERT INTO "pdscan_domain" VALUES (1, '8d6f480c', 'bitwarden-bronya-rayi-1.rayi.vip', '47.104.134.135');
INSERT INTO "pdscan_domain" VALUES (2, 'dc8a81a8', 'bitwarden-bronya-rayi-1.rayi.vip', '47.104.134.135');
INSERT INTO "pdscan_domain" VALUES (3, 'dc8a81a8', 'gitea.rayi.vip', '47.104.134.135');
INSERT INTO "pdscan_domain" VALUES (4, 'dc8a81a8', 'js.rayi.vip', '47.104.134.135');
INSERT INTO "pdscan_domain" VALUES (5, 'dc8a81a8', 'rayi.vip', '47.104.134.135');
INSERT INTO "pdscan_domain" VALUES (6, 'dc8a81a8', 'www.rayi.vip', '47.104.134.135');
INSERT INTO "pdscan_domain" VALUES (7, 'dc8a81a8', 'www.xss.rayi.vip', 'www.xss.rayi.vip,www.xss.rayi.vip');

-- ----------------------------
-- Table structure for pdscan_ip
-- ----------------------------
DROP TABLE IF EXISTS "pdscan_ip";
CREATE TABLE "pdscan_ip" (
  "id" INTEGER NOT NULL,
  "task_id" text NOT NULL,
  "ip" VARCHAR,
  "port" INTEGER,
  "service" VARCHAR,
  "banner" VARCHAR,
  PRIMARY KEY ("id")
);

-- ----------------------------
-- Records of pdscan_ip
-- ----------------------------
INSERT INTO "pdscan_ip" VALUES (1, '8d6f480c', '47.104.134.135', 3389, 'ssh', 'SSH-2.0-OpenSSH_8.2p1 Ubuntu-4ubuntu0.3\x0d\x0a');
INSERT INTO "pdscan_ip" VALUES (2, '8d6f480c', '47.104.134.135', 3389, 'ssh', 'SSH-2.0-OpenSSH_8.2p1 Ubuntu-4ubuntu0.3\x0d\x0a');
INSERT INTO "pdscan_ip" VALUES (3, '8d6f480c', '47.104.134.135', 443, 'http', '');
INSERT INTO "pdscan_ip" VALUES (4, '8d6f480c', '47.104.134.135', 80, 'http', '');
INSERT INTO "pdscan_ip" VALUES (5, 'dc8a81a8', '47.104.134.135', 3389, 'ssh', 'SSH-2.0-OpenSSH_8.2p1 Ubuntu-4ubuntu0.3\x0d\x0a');
INSERT INTO "pdscan_ip" VALUES (6, 'dc8a81a8', '47.104.134.135', 443, 'http', '');
INSERT INTO "pdscan_ip" VALUES (7, 'dc8a81a8', '47.104.134.135', 80, 'http', '');

-- ----------------------------
-- Table structure for pdscan_site
-- ----------------------------
DROP TABLE IF EXISTS "pdscan_site";
CREATE TABLE "pdscan_site" (
  "id" INTEGER NOT NULL,
  "task_id" text NOT NULL,
  "url" TEXT NOT NULL,
  "ip" TEXT,
  "status_code" TEXT,
  "title" TEXT,
  "finger" TEXT,
  PRIMARY KEY ("id")
);

-- ----------------------------
-- Records of pdscan_site
-- ----------------------------
INSERT INTO "pdscan_site" VALUES (1, '8d6f480c', 'http://47.104.134.135:80', '47.104.134.135:80', 200, '404NotFound', 'server:nginx

');
INSERT INTO "pdscan_site" VALUES (2, '8d6f480c', 'https://47.104.134.135:443', '47.104.134.135:443', 500, '500InternalServerError', 'server:nginx

');
INSERT INTO "pdscan_site" VALUES (3, 'dc8a81a8', 'http://47.104.134.135:80', '47.104.134.135:80', 200, '404NotFound', 'server:nginx

');
INSERT INTO "pdscan_site" VALUES (4, 'dc8a81a8', 'https://47.104.134.135:443', '47.104.134.135:443', 500, '500InternalServerError', 'server:nginx

');

-- ----------------------------
-- Table structure for pdscan_task
-- ----------------------------
DROP TABLE IF EXISTS "pdscan_task";
CREATE TABLE "pdscan_task" (
  "task_id" VARCHAR(255) NOT NULL,
  "task_name" VARCHAR(255) NOT NULL,
  "task_target" VARCHAR NOT NULL,
  "task_target_domain" VARCHAR,
  "task_target_ip" VARCHAR,
  "task_result_count" INTEGER,
  "task_running_module" VARCHAR(255) NOT NULL,
  "task_status" VARCHAR(255) NOT NULL,
  "task_start_time" VARCHAR(255) NOT NULL,
  "task_end_time" VARCHAR(255),
  "task_c_duan" VARCHAR,
  PRIMARY KEY ("task_id")
);

-- ----------------------------
-- Records of pdscan_task
-- ----------------------------
INSERT INTO "pdscan_task" VALUES ('8d6f480c', '测试任务', '["47.104.134.135", "rayi.vip"]', '["rayi.vip"]', '["47.104.134.135"]', NULL, 'portscan_done', 'Waiting', '2022-07-28 10:54:52', NULL, '["47.104.134.0/24"]');
INSERT INTO "pdscan_task" VALUES ('ffdf3a45', '测试2', '["rayi.vip"]', '["rayi.vip"]', '[]', NULL, 'portscan_done', 'Waiting', '2022-07-28 11:51:11', NULL, '[]');
INSERT INTO "pdscan_task" VALUES ('dc8a81a8', 'test', '["rayi.vip"]', '["rayi.vip"]', '[]', NULL, 'portscan_done', 'Waiting', '2022-07-28 12:18:07', NULL, '["47.104.134.0/24"]');

-- ----------------------------
-- Table structure for rt_power
-- ----------------------------
DROP TABLE IF EXISTS "rt_power";
CREATE TABLE "rt_power" (
  "id" INTEGER NOT NULL,
  "name" VARCHAR(255),
  "type" SMALLINT,
  "code" VARCHAR(30),
  "url" VARCHAR(255),
  "open_type" VARCHAR(10),
  "parent_id" INTEGER,
  "icon" VARCHAR(128),
  "sort" INTEGER,
  "enable" BOOLEAN,
  PRIMARY KEY ("id"),
  FOREIGN KEY ("parent_id") REFERENCES "rt_power" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION
);

-- ----------------------------
-- Records of rt_power
-- ----------------------------
INSERT INTO "rt_power" VALUES (1, '系统管理', 0, '', '', '', 0, 'layui-icon layui-icon-set-fill', 5, 1);
INSERT INTO "rt_power" VALUES (3, '用户管理', 1, 'admin:user:main', '/users/', '_iframe', 1, 'layui-icon layui-icon layui-icon layui-icon layui-icon-rate', 1, 1);
INSERT INTO "rt_power" VALUES (4, '权限管理', 1, 'admin:power:main', '/rights/', '_iframe', 1, NULL, 2, 1);
INSERT INTO "rt_power" VALUES (9, '角色管理', 1, 'admin:role:main', '/admin/role', '_iframe', 1, 'layui-icon layui-icon-username', 2, 1);
INSERT INTO "rt_power" VALUES (13, '日志管理', 1, 'admin:log:main', '/logs', '_iframe', 1, 'layui-icon layui-icon-read', 4, 1);
INSERT INTO "rt_power" VALUES (18, '图片上传', 1, 'admin:file:main', '/file', '_iframe', 17, 'layui-icon layui-icon-camera', 5, 1);
INSERT INTO "rt_power" VALUES (21, '权限增加', 2, 'admin:power:add', '', '', 4, 'layui-icon layui-icon-add-circle', 1, 1);
INSERT INTO "rt_power" VALUES (22, '用户增加', 2, 'admin:user:add', '', '', 3, 'layui-icon layui-icon-add-circle', 1, 1);
INSERT INTO "rt_power" VALUES (23, '用户编辑', 2, 'admin:user:edit', '', '', 3, 'layui-icon layui-icon-rate', 2, 1);
INSERT INTO "rt_power" VALUES (24, '用户删除', 2, 'admin:user:remove', '', '', 3, 'layui-icon None', 3, 1);
INSERT INTO "rt_power" VALUES (25, '权限编辑', 2, 'admin:power:edit', '', '', 4, 'layui-icon layui-icon-edit', 2, 1);
INSERT INTO "rt_power" VALUES (26, '用户删除', 2, 'admin:power:remove', '', '', 4, 'layui-icon layui-icon-delete', 3, 1);
INSERT INTO "rt_power" VALUES (27, '用户增加', 2, 'admin:role:add', '', '', 9, 'layui-icon layui-icon-add-circle', 1, 1);
INSERT INTO "rt_power" VALUES (28, '角色编辑', 2, 'admin:role:edit', '', '', 9, 'layui-icon layui-icon-edit', 2, 1);
INSERT INTO "rt_power" VALUES (29, '角色删除', 2, 'admin:role:remove', '', '', 9, 'layui-icon layui-icon-delete', 3, 1);
INSERT INTO "rt_power" VALUES (30, '角色授权', 2, 'admin:role:power', '', '', 9, 'layui-icon layui-icon-component', 4, 1);
INSERT INTO "rt_power" VALUES (31, '图片增加', 2, 'admin:file:add', '', '', 18, 'layui-icon layui-icon-add-circle', 1, 1);
INSERT INTO "rt_power" VALUES (32, '图片删除', 2, 'admin:file:delete', '', '', 18, 'layui-icon layui-icon-delete', 2, 1);
INSERT INTO "rt_power" VALUES (48, '部门管理', 1, 'admin:dept:main', '/dept', '_iframe', 1, 'layui-icon layui-icon-group', 3, 1);
INSERT INTO "rt_power" VALUES (49, '部门增加', 2, 'admin:dept:add', '', '', 48, 'layui-icon None', 1, 1);
INSERT INTO "rt_power" VALUES (50, '部门编辑', 2, 'admin:dept:edit', '', '', 48, 'layui-icon ', 2, 1);
INSERT INTO "rt_power" VALUES (51, '部门删除', 2, 'admin:dept:remove', '', '', 48, 'layui-icon None', 3, 1);
INSERT INTO "rt_power" VALUES (52, '任务列表', 1, '', '/task/list', '_iframe', 0, 'layui-icon layui-icon-list', 1, 1);
INSERT INTO "rt_power" VALUES (53, '配置管理', 0, '', '', '', 0, 'layui-icon layui-icon-util', 2, 1);

-- ----------------------------
-- Table structure for rt_role
-- ----------------------------
DROP TABLE IF EXISTS "rt_role";
CREATE TABLE "rt_role" (
  "id" INTEGER NOT NULL,
  "name" VARCHAR(255),
  "code" VARCHAR(255),
  "enable" BOOLEAN,
  "comment" VARCHAR(255),
  "details" VARCHAR(255),
  "sort" INTEGER,
  PRIMARY KEY ("id")
);

-- ----------------------------
-- Records of rt_role
-- ----------------------------
INSERT INTO "rt_role" VALUES (1, '管理员', 'admin', 1, NULL, '管理员', 1);
INSERT INTO "rt_role" VALUES (2, '普通用户', 'common', 1, NULL, '只有查看，没有增删改权限', 2);

-- ----------------------------
-- Table structure for rt_role_power
-- ----------------------------
DROP TABLE IF EXISTS "rt_role_power";
CREATE TABLE "rt_role_power" (
  "id" INTEGER NOT NULL,
  "power_id" INTEGER,
  "role_id" INTEGER,
  PRIMARY KEY ("id"),
  FOREIGN KEY ("power_id") REFERENCES "rt_power" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION,
  FOREIGN KEY ("role_id") REFERENCES "rt_role" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION
);

-- ----------------------------
-- Records of rt_role_power
-- ----------------------------
INSERT INTO "rt_role_power" VALUES (241, 12, 1);
INSERT INTO "rt_role_power" VALUES (257, 44, 1);
INSERT INTO "rt_role_power" VALUES (258, 45, 1);
INSERT INTO "rt_role_power" VALUES (259, 46, 1);
INSERT INTO "rt_role_power" VALUES (260, 47, 1);
INSERT INTO "rt_role_power" VALUES (265, 1, 2);
INSERT INTO "rt_role_power" VALUES (266, 3, 2);
INSERT INTO "rt_role_power" VALUES (267, 4, 2);
INSERT INTO "rt_role_power" VALUES (268, 9, 2);
INSERT INTO "rt_role_power" VALUES (269, 12, 2);
INSERT INTO "rt_role_power" VALUES (270, 13, 2);
INSERT INTO "rt_role_power" VALUES (272, 18, 2);
INSERT INTO "rt_role_power" VALUES (273, 44, 2);
INSERT INTO "rt_role_power" VALUES (274, 48, 2);
INSERT INTO "rt_role_power" VALUES (275, 1, 1);
INSERT INTO "rt_role_power" VALUES (276, 3, 1);
INSERT INTO "rt_role_power" VALUES (277, 4, 1);
INSERT INTO "rt_role_power" VALUES (278, 9, 1);
INSERT INTO "rt_role_power" VALUES (279, 13, 1);
INSERT INTO "rt_role_power" VALUES (280, 21, 1);
INSERT INTO "rt_role_power" VALUES (281, 22, 1);
INSERT INTO "rt_role_power" VALUES (282, 23, 1);
INSERT INTO "rt_role_power" VALUES (283, 24, 1);
INSERT INTO "rt_role_power" VALUES (284, 25, 1);
INSERT INTO "rt_role_power" VALUES (285, 26, 1);
INSERT INTO "rt_role_power" VALUES (286, 27, 1);
INSERT INTO "rt_role_power" VALUES (287, 28, 1);
INSERT INTO "rt_role_power" VALUES (288, 29, 1);
INSERT INTO "rt_role_power" VALUES (289, 30, 1);
INSERT INTO "rt_role_power" VALUES (290, 48, 1);
INSERT INTO "rt_role_power" VALUES (291, 49, 1);
INSERT INTO "rt_role_power" VALUES (292, 50, 1);
INSERT INTO "rt_role_power" VALUES (293, 51, 1);
INSERT INTO "rt_role_power" VALUES (294, 52, 1);
INSERT INTO "rt_role_power" VALUES (295, 53, 1);

-- ----------------------------
-- Table structure for rt_user_role
-- ----------------------------
DROP TABLE IF EXISTS "rt_user_role";
CREATE TABLE "rt_user_role" (
  "id" INTEGER NOT NULL,
  "user_id" INTEGER,
  "role_id" INTEGER,
  PRIMARY KEY ("id"),
  FOREIGN KEY ("role_id") REFERENCES "rt_role" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION,
  FOREIGN KEY ("user_id") REFERENCES "cp_user" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION
);

-- ----------------------------
-- Records of rt_user_role
-- ----------------------------
INSERT INTO "rt_user_role" VALUES (21, 1, 1);

PRAGMA foreign_keys = true;
