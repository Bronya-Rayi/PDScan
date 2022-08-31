-- ----------------------------
-- Table structure for pdscan_domain
-- ----------------------------
DROP TABLE IF EXISTS "pdscan_domain";
CREATE TABLE "pdscan_domain" (
  "domain" VARCHAR NOT NULL,
  "domain_record" VARCHAR NOT NULL,
  "task_id" VARCHAR NOT NULL,
  PRIMARY KEY ("domain")
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
  "ip" VARCHAR,
  "domain" VARCHAR,
  "port" INTEGER,
  "os" VARCHAR,
  "protocol" VARCHAR,
  "product_name" VARCHAR,
  "application_component" VARCHAR,
  "app_digest" VARCHAR,
  "banner" VARCHAR,
  "url_scan" VARCHAR,
  "task_id" VARCHAR,
  PRIMARY KEY ("id"),
  UNIQUE ("ip" ASC)
);

-- ----------------------------
-- Records of pdscan_ip
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
  PRIMARY KEY ("task_id")
);
