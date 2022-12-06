CREATE TABLE `channel` (
  `id` INT PRIMARY KEY NOT NULL,
  `owner_id` INT,
  `member_id` int,
  `name` VARCHAR(50) NOT NULL,
  `description` VARCHAR(50),
  `created_at` DATETIME,
  `updated_at` DATETIME
);

CREATE TABLE `user` (
  `user_id` INT,
  `ID` INT PRIMARY KEY NOT NULL AUTO_INCREMENT,
  `nickname` String NOT NULL,
  `no_tlp` VARCHAR(12) NOT NULL,
  `pin` VARCHAR(40) NOT NULL,
  `name` VARCHAR(20) NOT NULL DEFAULT "",
  `created_at` DATETIME NOT NULL,
  `updated_at` DATETIME NOT NULL,
  `contact_id` INT,
  `channel_id` INT
);

CREATE TABLE `user_contact` (
  `user_id` INT NOT NULL,
  `contact_id` INT PRIMARY KEY,
  `created_at` DATETIME NOT NULL,
  `updated_at` DATETIME NOT NULL
);

ALTER TABLE `channel` ADD FOREIGN KEY (`owner_id`) REFERENCES `user` (`user_id`);

ALTER TABLE `channel` ADD FOREIGN KEY (`id`) REFERENCES `user` (`channel_id`);

ALTER TABLE `user` ADD FOREIGN KEY (`channel_id`) REFERENCES `channel` (`member_id`);

ALTER TABLE `user` ADD FOREIGN KEY (`contact_id`) REFERENCES `user_contact` (`contact_id`);
