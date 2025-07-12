-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jul 12, 2025 at 12:48 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `re_wear`
--

-- --------------------------------------------------------

--
-- Table structure for table `items`
--

CREATE TABLE `items` (
  `id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `name` varchar(100) DEFAULT NULL,
  `description` text DEFAULT NULL,
  `image_filename` varchar(255) DEFAULT NULL,
  `category` varchar(100) DEFAULT NULL,
  `approved` tinyint(1) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `items`
--

INSERT INTO `items` (`id`, `user_id`, `name`, `description`, `image_filename`, `category`, `approved`) VALUES
(2, 1, 'Shirt', 'Good condition', 'shirt.jpg', 'Casual Shirt', 0),
(3, 1, 'Shirt', 'Good Condition', '1.jpg', 'Casual Shirt', 0),
(4, 1, 'Shirt', 'Good Condition', '2.jpg', 'Casual Shirt', 0),
(5, 1, 'Shirt', 'Good Condition', '4.jpg', 'Casual Shirt', 0),
(6, 1, 'Shirt', 'Good Condition', '3.jpg', 'Casual Shirt', 0),
(7, 1, 'Shirt', 'Good Condition', '5.jpg', 'Casual Shirt', 0),
(8, 1, 'Shirt', 'Good Condition', '6.jpg', 'Casual Shirt', 0),
(9, 1, 'Shirt', 'Good Condition', '7.jpg', 'Casual Shirt', 0),
(10, 1, 'Shirt', 'Good Condition', '8.jpg', 'Casual Shirt', 0),
(11, 1, 'Shirt', 'Good Condition', '9.jpg', 'Casual Shirt', 0),
(12, 1, 'Shirt', 'Good Condition', '10.jpg', 'Casual Shirt', 0),
(13, 2, 'Dress', 'Used 1-2 Times', 'f1.jpg', 'Dress Women', 0),
(14, 2, 'Dress', 'Used 1-2 Times', 'f2.jpg', 'Dress Women', 0),
(15, 2, 'Dress', 'Used 1-2 Times', 'f3.jpg', 'Dress Women', 0),
(16, 2, 'Dress', 'Used 1-2 Times', 'f4.jpg', 'Dress Women', 0),
(17, 2, 'Dress', 'Used 1-2 Times', 'f5.jpg', 'Dress Women', 0),
(18, 2, 'Dress', 'Used 1-2 Times', 'f6.jpg', 'Dress Women', 0),
(19, 2, 'Dress', 'Used 1-2 Times', 'f7.jpg', 'Dress Women', 0),
(20, 2, 'Dress', 'Used 1-2 Times', 'f8.jpg', 'Dress Women', 0),
(21, 2, 'Dress', 'Used 1-2 Times', 'f9.jpg', 'Dress Women', 0),
(22, 2, 'Dress', 'Used 1-2 Times', 'f10.jpg', 'Dress Women', 0),
(23, 3, 'T-shirt', 'Used', 't1.jpg', 'T-Shirt Men', 0),
(24, 3, 'T-shirt', 'Used', 't2.jpg', 'T-Shirt Men', 0),
(25, 3, 'T-shirt', 'Used', 't3.jpg', 'T-Shirt Men', 0),
(26, 3, 'T-shirt', 'Used', 't4.jpg', 'T-Shirt Men', 0),
(27, 3, 'T-shirt', 'Used', 't5.jpg', 'T-Shirt Men', 0),
(28, 3, 'T-shirt', 'Used', 't6.jpg', 'T-Shirt Men', 0),
(29, 3, 'T-shirt', 'Used', 't7.jpg', 'T-Shirt Men', 0),
(30, 3, 'T-shirt', 'Used', 't8.jpg', 'T-Shirt Men', 0),
(31, 3, 'T-shirt', 'Used', 't9.jpg', 'T-Shirt Men', 0),
(32, 3, 'T-shirt', 'Used', 't10.jpg', 'T-Shirt Men', 0),
(35, 4, 'Unisex', 'New', 'u3.jpg', 'Unisex', 0),
(36, 4, 'Unisex', 'New', 'u4.jpg', 'Unisex', 0),
(37, 4, 'Unisex', 'New', 'u5.jpg', 'Unisex', 0),
(38, 4, 'Unisex', 'New', 'u6.jpg', 'Unisex', 0),
(39, 4, 'Unisex', 'New', 'u7.jpg', 'Unisex', 0),
(40, 4, 'Unisex', 'New', 'u8.jpg', 'Unisex', 1),
(41, 4, 'Unisex', 'New', 'u9.jpg', 'Unisex', 0);

-- --------------------------------------------------------

--
-- Table structure for table `requests`
--

CREATE TABLE `requests` (
  `id` int(11) NOT NULL,
  `item_id` int(11) DEFAULT NULL,
  `requester_id` int(11) DEFAULT NULL,
  `status` enum('pending','approved','rejected') DEFAULT 'pending',
  `request_date` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `requests`
--

INSERT INTO `requests` (`id`, `item_id`, `requester_id`, `status`, `request_date`) VALUES
(1, 13, 1, 'pending', '2025-07-12 10:30:21'),
(2, 31, 1, '', '2025-07-12 10:34:28');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `name` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `points` int(11) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `name`, `email`, `password`, `points`) VALUES
(1, 'Prince', 'princegajera0506@gmail.com', '$2b$12$3rHKjlCqRCK.BiMXMpCmwO6/eoNlkZ0L1vDjR5S1QD2Wr1gyDBOS2', 10),
(2, 'Pari Metaliya', 'parimetaliya@gmail.com', '$2b$12$nvosTi2ZeVZ/WW7pzbByTuOu4YLp9ex6LhPgSiv8k7c8UUAGN1Iru', 0),
(3, 'Mayank', 'mayankchauhan966@gmail.com', '$2b$12$46I/Ogn7dezRwzXURGnoR.S3MQTgn.Ue88Q/InV1qoFJGIbd7QST.', 0),
(4, 'Bhargav', 'bhargavvv412@gmail.com', '$2b$12$G4jnYORRRGTsTC.I4YdvSuXknVGy0cW5KCmPFQ9yvkKZqwuXJVc2G', 0);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `items`
--
ALTER TABLE `items`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `requests`
--
ALTER TABLE `requests`
  ADD PRIMARY KEY (`id`),
  ADD KEY `item_id` (`item_id`),
  ADD KEY `requester_id` (`requester_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `items`
--
ALTER TABLE `items`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=43;

--
-- AUTO_INCREMENT for table `requests`
--
ALTER TABLE `requests`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `items`
--
ALTER TABLE `items`
  ADD CONSTRAINT `items_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

--
-- Constraints for table `requests`
--
ALTER TABLE `requests`
  ADD CONSTRAINT `requests_ibfk_1` FOREIGN KEY (`item_id`) REFERENCES `items` (`id`),
  ADD CONSTRAINT `requests_ibfk_2` FOREIGN KEY (`requester_id`) REFERENCES `users` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
