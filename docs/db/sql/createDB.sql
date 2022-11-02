
/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;


-- trdb 데이터베이스 
CREATE DATABASE IF NOT EXISTS `trdb` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `trdb`;


-- 테이블 trdb.user 
CREATE TABLE IF NOT EXISTS user (
    user_id INT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '회원아이디',
    user_nm VARCHAR(20) NOT NULL COMMENT '로그인아이디',
    password VARCHAR(45) NOT NULL COMMENT '비밀번호',
    name VARCHAR(20) NOT NULL COMMENT '이름',
    email VARCHAR(45) NOT NULL COMMENT '이메일',
    country_cd INT UNSIGNED DEFAULT 82 COMMENT '국가번호',
    tel INT UNSIGNED NOT NULL COMMENT '전화번호',
    zipcode VARCHAR(20) DEFAULT NULL COMMENT '우편번호',
    address VARCHAR(255) DEFAULT NULL COMMENT '주소',
    addr_detail VARCHAR(45) DEFAULT NULL COMMENT '상세주소',
    birth_dt INT UNSIGNED DEFAULT NULL COMMENT '생년월일',
    role TINYINT UNSIGNED DEFAULT 0 COMMENT '권한(일반:0,관리자:1)',
    reg_dt DATETIME DEFAULT NOW COMMENT '등록일자',
    del_dt DATETIME DEFAULT NULL COMMENT '탈퇴일자',
    PRIMARY KEY (user_id),
    UNIQUE KEY user_nm (user_nm)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='회원정보';


-- 테이블 trdb.place 
CREATE TABLE IF NOT EXISTS place (
    place_id INT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '관광지아이디',
    place_nm VARCHAR(128) NOT NULL COMMENT '관광지명',
    city VARCHAR(10) NOT NULL COMMENT '도시',
    theme VARCHAR(10) DEFAULT NULL COMMENT '테마',
    province VARCHAR(10) NOT NULL COMMENT '도',
    road_addr VARCHAR(255) DEFAULT NULL COMMENT '도로명주소',
    addr VARCHAR(255) DEFAULT NULL COMMENT '지번주소',
    lat DOUBLE DEFAULT NULL COMMENT '위도',
    long DOUBLE DEFAULT NULL COMMENT '경도',
    srch_cnt INT UNSIGNED DEFAULT NULL COMMENT '검색건수',
    score FLOAT DEFAULT NULL COMMENT '별점',
    review_cnt INT UNSIGNED DEFAULT NULL COMMENT '리뷰수',
    class VARCHAR(10) DEFAULT NULL COMMENT '카테고리',
    info VARCHAR(255) DEFAULT NULL COMMENT '소개',
    reg_dt DATETIME DEFAULT NOW COMMENT '등록일자',
    update_dt DATETIME DEFAULT NULL COMMENT '수정일자',
    add_cnt INT UNSIGNED DEFAULT 0 COMMENT '관심등록수',
    PRIMARY KEY (place_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='관광지';


-- 테이블 trdb.myplace 
CREATE TABLE IF NOT EXISTS myplace (
    user_id INT UNSIGNED NOT NULL COMMENT '회원아이디',
    place_id INT UNSIGNED NOT NULL COMMENT '관광지아이디',
    KEY FK_user_TO_myplace (user_id),
    KEY FK_place_TO_myplace (place_id),
    CONSTRAINT FK_user_TO_myplace FOREIGN KEY (user_id) REFERENCES user (user_id) ON DELETE RESTRICT ON UPDATE RESTRICT,
    CONSTRAINT FK_place_TO_myplace FOREIGN KEY (place_id) REFERENCES place (place_id) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='관심장소';


-- 테이블 trdb.mytrip 
CREATE TABLE IF NOT EXISTS mytrip (
    trip_id INT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '여행아이디',
    user_id INT UNSIGNED NOT NULL COMMENT '회원아이디',
    PRIMARY KEY (trip_id),
    KEY FK_user_TO_mytrip (user_id),
    CONSTRAINT FK_user_TO_mytrip FOREIGN KEY (user_id) REFERENCES user (user_id) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='여행경로';
-- 추가 컬럼 정의 필요


-- 테이블 trdb.board 
CREATE TABLE IF NOT EXISTS board (
    board_id INT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '게시판아이디',
    writer VARCHAR(20) NOT NULL COMMENT '작성자',
    title VARCHAR(150) NOT NULL COMMENT '제목',
    content TEXT NOT NULL COMMENT '내용',
    secret_yn BOOLEAN DEFAULT 0 COMMENT '비밀글여부',
    passwd INT DEFAULT NULL COMMENT '비밀번호',
    view_cnt INT DEFAULT NULL COMMENT '조회수',
    reg_dt DATETIME DEFAULT NOW COMMENT '등록일자',
    update_dt DATETIME DEFAULT NULL COMMENT '수정일자',
    PRIMARY KEY (board_id),
    KEY FK_user_TO_board (writer),
    CONSTRAINT FK_user_TO_board FOREIGN KEY (writer) REFERENCES user (user_nm) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='게시판';


-- 테이블 trdb.reply 
CREATE TABLE IF NOT EXISTS reply (
    reply_id INT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '댓글아이디',
    board_id INT UNSIGNED NOT NULL COMMENT '게시판아이디',
    writer VARCHAR(20) NOT NULL COMMENT '작성자',
    content TEXT NOT NULL COMMENT '내용',
    reg_dt DATETIME DEFAULT NOW COMMENT '등록일자',
    update_dt DATETIME DEFAULT NULL COMMENT '수정일자',
    PRIMARY KEY (reply_id),
    KEY FK_user_TO_reply (writer),
    KEY FK_board_TO_reply (board_id),
    CONSTRAINT FK_user_TO_reply FOREIGN KEY (writer) REFERENCES user (user_nm) ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT FK_board_TO_reply FOREIGN KEY (board_id) REFERENCES board (board_id) ON DELETE CASCADE ON UPDATE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='댓글';


-- 테이블 trdb.group 
CREATE TABLE IF NOT EXISTS group (
    group_id INT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '그룹아이디',
    group_nm VARCHAR(20)  NOT NULL COMMENT '그룹명',
    reg_dt DATETIME DEFAULT NOW COMMENT '등록일자',
    update_dt DATETIME DEFAULT NULL COMMENT '수정일자',
    PRIMARY KEY (group_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='그룹';


-- 테이블 trdb.user_group 
CREATE TABLE IF NOT EXISTS user_group (
    user_id INT UNSIGNED NOT NULL COMMENT '회원아이디',
    group_id INT UNSIGNED NOT NULL COMMENT '그룹아이디',
    KEY FK_user_TO_user_group (user_id),
    KEY FK_group_TO_user_group (group_id),
    CONSTRAINT FK_user_TO_user_group FOREIGN KEY (user_id) REFERENCES user (user_id) ON DELETE RESTRICT ON UPDATE RESTRICT,
    CONSTRAINT FK_group_TO_user_group FOREIGN KEY (group_id) REFERENCES group (group_id) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='그룹관계';
-- 필요 시 추가 컬럼 정의
