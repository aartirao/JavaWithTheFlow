#Procedure for updating/inserting the user rating score
USE ANS;
DELIMITER //
CREATE PROCEDURE `sp_UpdateUserRatingScore` (IN AnswerId INT
, IN UId INT, IN Score INT)
BEGIN
	DECLARE ret INT;
    
    IF EXISTS ( SELECT Id FROM UserRatingsScore WHERE PostId = AnswerId AND UserId = UId ) THEN
		UPDATE UserRatingsScore SET Rating = Score WHERE 
        UserId = UId AND PostId = AnswerId;
        SET ret = 1;
	ELSE
		INSERT INTO UserRatingsScore (UserId, PostId, Rating, CreationDate)
        VALUES (UId, AnswerId, Score, NOW());
        SET ret = 1;
    END IF;
    SELECT ret;
END //
DELIMITER ;