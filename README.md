# Boolean Information Retrieval System

A high-performance Information Retrieval (IR) system built in Python that supports Boolean logic and proximity searches. The system features a multithreaded indexing engine, custom linked-list-based posting lists, and a user-friendly Tkinter GUI.


## 🚀 Features

* **Multithreaded Indexing**: Efficiently parses document corpora using Python's `threading` library to speed up the creation of the inverted index.
* **Positional Indexing**: Supports proximity queries (e.g., finding words within a distance of $k$).
* **Custom Data Structures**: Implements posting lists using a manual Linked List for optimized memory and traversal during Boolean operations.
* **Text Preprocessing**: Includes a full pipeline of tokenization, case folding, stopword removal, and Porter Stemming via `NLTK`.
* **Interactive GUI**: A built-in Tkinter application for real-time querying and result visualization.

## 📂 Project Structure

```text
├── Abstracts/                # Directory containing .txt document corpus
├── Stopword-List.txt         # List of words to be excluded from indexing
├── Gold Query-Set...         # Benchmark queries and expected results
├── linked_list.py            # Custom Node and Linked List implementation
├── model.py                  # Core engine: Indexing, logic, and query processing
└── main.py                   # GUI Application and Entry Point
```

## 🛠️ Installation & Setup

### Prerequisites
* Python 3.8+
* The system uses `NLTK` for Natural Language Processing.

### 1. Clone the Repository
```bash
git clone https://github.com/sherrytelli/boolean-retrieval-model.git
cd boolean-retrieval-system
```

### 2. Set Up a Virtual Environment (Recommended)
**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Required Libraries
```bash
pip install nltk natsort
```

### 4. Download NLTK Data
The project requires the `punkt` tokenizer. Run this command once in your terminal:
```bash
python -c "import nltk; nltk.download('punkt')"
```

---

## 🔍 Usage & Query Syntax

Run the application:
```bash
python main.py
```

The system supports several query formats in the GUI:

| Query Type | Syntax Example | Description |
| :--- | :--- | :--- |
| **Single Word** | `machine` | Returns all documents containing "machine". |
| **Two-word Boolean** | `machine and learning` | Returns intersection of both terms. |
| **Three-word Boolean** | `data or science andnot art` | Complex logic with three terms. |
| **Proximity Query** | `natural language /3` | Returns docs where words are within 3 positions. |

**Supported Operators**: `and`, `or`, `andnot`.

---

## 🏗️ Technical Architecture

1.  **Parsing**: Documents are read from the `Abstracts/` folder. The `model.py` script uses `PorterStemmer` to normalize terms.
2.  **Indexing**: A `Positional Index` is built where each term maps to a Linked List of Nodes. Each Node contains the Document ID and a list of specific word positions.
3.  **Optimization**: 
    * **Boolean Query Optimization**: For three-word queries, the system compares the sizes of the posting lists to determine the most efficient order of operations.
    * **Positional Intersect**: Uses a "distance-aware" intersection algorithm to fulfill `/k` proximity requirements.

---

## 📝 License
Distributed under the MIT License. See `LICENSE` for more information.