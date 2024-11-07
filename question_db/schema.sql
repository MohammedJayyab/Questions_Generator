-- Create `books` table
CREATE TABLE books (
    book_id INT NOT NULL AUTO_INCREMENT,
    title VARCHAR(255) NOT NULL,
    author VARCHAR(255),
    publication_year VARCHAR(20),
    isbn VARCHAR(20),
    total_chapters INT,
    PRIMARY KEY (book_id)
);

-- Create `chapters` table
CREATE TABLE chapters (
    chapter_id INT NOT NULL AUTO_INCREMENT,
    book_id INT NOT NULL,
    chapter_number INT NOT NULL,
    title VARCHAR(255),
    page_start INT,
    page_end INT,
    PRIMARY KEY (chapter_id),
    FOREIGN KEY (book_id) REFERENCES books(book_id) ON DELETE CASCADE
);

-- Create `topics` table
CREATE TABLE topics (
    topic_id INT NOT NULL AUTO_INCREMENT,
    chapter_id INT NOT NULL,
    topic_title VARCHAR(255) NOT NULL,
    content TEXT,
    page_start INT,
    page_end INT,
    PRIMARY KEY (topic_id),
    FOREIGN KEY (chapter_id) REFERENCES chapters(chapter_id) ON DELETE CASCADE
);

-- Create `mcqs` table
CREATE TABLE mcqs (
    mcq_id INT NOT NULL AUTO_INCREMENT,
    topic_id INT NOT NULL,
    question TEXT NOT NULL,
    difficulty VARCHAR(50),
    PRIMARY KEY (mcq_id),
    FOREIGN KEY (topic_id) REFERENCES topics(topic_id) ON DELETE CASCADE
);

-- Create `mcq_options` table
CREATE TABLE mcq_options (
    option_id INT NOT NULL AUTO_INCREMENT,
    mcq_id INT NOT NULL,
    option_text TEXT NOT NULL,
    is_correct BOOLEAN DEFAULT FALSE,
    PRIMARY KEY (option_id),
    FOREIGN KEY (mcq_id) REFERENCES mcqs(mcq_id) ON DELETE CASCADE
);

-- Create `annotations` table
CREATE TABLE annotations (
    annotation_id INT NOT NULL AUTO_INCREMENT,
    topic_id INT NOT NULL,
    note TEXT NOT NULL,
    page_number INT,
    PRIMARY KEY (annotation_id),
    FOREIGN KEY (topic_id) REFERENCES topics(topic_id) ON DELETE CASCADE
);
