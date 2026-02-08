# Procedure 01: The Librarian (Gathering)

**Objective:**
Collect raw materials (Specific & General) and file them into the `IdeaBox`.
The user just dumps the info; the AI formats and saves it.

## 📥 Logic Flow

### 1. Receive Input (Raw Material)
*   User Input: "Takes notes", "Pastes URL", "Random thought".
*   User Command: "素材追加", "Gather", "メモ".

### 2. Classification & Formatting
*   Detect if the input is:
    *   **Type A: Specific (特殊的)** -> Relates to the Core Problem (Job/Product).
    *   **Type B: General (一般的)** -> Totally unrelated (History, Bio, News).
*   Format as **Digital Card**:
    ```markdown
    # Card: {Title}
    *   **Type:** {Specific or General}
    *   **Source:** {URL or Context}
    *   **Fact:** {Objective Data}
    *   **Insight:** {Why is this interesting?}
    ```

### 3. Filing (Save Action)
*   **Path:** `g:\マイドライブ\Genesis_OS\10_Domains\01_Work\04_IdeaBox\Cards\YYYYMMDD_{Title}.md`
*   **Action:** Use `write_to_file` to save the card.

### 4. Transition
*   Ask: "More materials? Or proceed to Mastication?"
*   If "Mastication" -> Load `02_MASTICATING.md`.
