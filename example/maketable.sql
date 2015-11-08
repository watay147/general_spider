CREATE TABLE IF NOT EXISTS `update000415` (
  `title` varchar(80) NOT NULL,
  `articleid` varchar(80) NOT NULL,
  `stockno` varchar(8) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE IF NOT EXISTS `update2` (
  `reply` int(11) NOT NULL,
  `click` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `update3` (
  `title` varchar(100) NOT NULL,
  `content` text NOT NULL,
  `author` varchar(40) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;