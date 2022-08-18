データベース設計

１）ボトムアップアプローチ
  既存の伝票を非正規形→第一正規形→第二正規形→第三正規形

２）トップダウンアプローチ
  全くゼロから設計をする（既存のものがない）



create table schedule(
  id         int           NOT NULL AUTO_INCREMENT,
  date_ID    int           NOT NULL,
  kinds      nvarchar(10)  NOT NULL,
  contents   nvarchar(255) NOT NULL,
  user_ID    int           NOT NULL,
  PRIMARY KEY(id),
  FOREIGN KEY(date_ID) REFERENCES calendar(date_ID),
  FOREIGN KEY(user_ID) REFERENCES user(user_ID)
);


create table calendar(
  date_ID int not null auto_increment,
  date    date   NOT NULL,
  PRIMARY KEY(date_ID)
);

create table user (
  user_ID  int not null auto_increment,
  user_name nvarchar(10)  not null,
  user_password varchar(20) not null,
  PRIMARY KEY (user_ID)
);
