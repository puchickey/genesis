# Procedure 02: The Shuffler (Masticating)

**Objective:**
Force the brain to find new relationships.
Use 3 distinct modes to vary the stimulation level.

## 🥣 Logic Flow

### 1. Mode Selection (Auto-Detect)
*   **Default:** Start with **Mode A (The Mixer)**.
*   **Trigger "Deepen":** If user picks a specific pair -> Switch to **Mode B (SCAMPER)**.
*   **Trigger "Stuck":** If user says "Nothing", "Bored", "煮詰まった" -> Switch to **Mode C (The Jolt)**.

---

### 🟢 Mode A: The Mixer (Combinatorial)
*   **Action:** Pick 3-5 cards and list ALL combinations (nCr).
*   **Question:** "What happens if [A] is applied to [B]?"

---

### 🟡 Mode B: The Transformer (SCAMPER)
*   **Trigger:** User wants to deep-dive into one idea or pair.
*   **Action:** Apply ONE of the following lenses (Cycle through them). Do not generate random questions; use these templates:

| Lens | Template Question |
| :--- | :--- |
| **S (Substitute)** | "Can we replace a human element in this idea with an AI/System?" |
| **C (Combine)** | "Can we bundle this with a completely different service (e.g., Coffee, Gym)?" |
| **A (Adapt)** | "How would Netflix/Uber handle this specific problem?" |
| **M (Modify)** | "What if we exaggerate the defining feature by 10x?" |
| **P (Put to other use)** | "If this product failed, how could we sell the 'waste' or 'process'?" |
| **E (Eliminate)** | "Remove the 'Core Feature'. What is left? Can that be the value?" |
| **R (Reverse)** | "What if the customer pays the vendor? (Reverse the flow)" |

---

### 🔴 Mode C: The Jolt (Random Word)
*   **Trigger:** ONLY when the user is explicitly "Stuck".
*   **Constraint:** Do not use this mode unless requested or stuck.
*   **Action:**
    1.  Pick a random noun totally unrelated to work (e.g., Hippo, Soap, Mars, Ramen).
    2.  Force a connection: "How is [Project] like a [Random Noun]?"

---

### 2. Transition
*   When the user says "もう無理 (Impossible)", "疲れた (Tired)":
*   **Action:** Force Transition to Incubation.
*   > `view_file g:\マイドライブ\Genesis_OS\.agent\skills\young-method\procedures\03_INCUBATING.md`
