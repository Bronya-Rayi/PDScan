/*
 Navicat Premium Data Transfer

 Source Server         : database
 Source Server Type    : SQLite
 Source Server Version : 3030001
 Source Schema         : main

 Target Server Type    : SQLite
 Target Server Version : 3030001
 File Encoding         : 65001

 Date: 28/07/2022 23:24:50
*/

PRAGMA foreign_keys = false;

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS "user";
CREATE TABLE "user" (
  "id" INTEGER NOT NULL,
  "username" VARCHAR(20),
  "password_hash" VARCHAR(128),
  PRIMARY KEY ("id")
);

-- ----------------------------
-- Records of user
-- ----------------------------
INSERT INTO "user" VALUES (1, 'admin', 'pbkdf2:sha256:150000$raM7mDSr$58fe069c3eac01531fc8af85e6fc200655dd2588090530084d182e6ec9d52c85');

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
  "task_port_limit" TEXT,
  "task_vulscan" TEXT,
  PRIMARY KEY ("task_id")
);

-- ----------------------------
-- Records of pdscan_task
-- ----------------------------
INSERT INTO "pdscan_task" VALUES ('3829a4e0', 'test1', '["rayi.vip"]', '["rayi.vip"]', '[]', NULL, 'subdomain', 'Paused', '2022-07-28 22:51:33', NULL, NULL, 'FULL_PORT', NULL);