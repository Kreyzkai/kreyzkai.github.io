# Copilot Instructions for KreyziKai.Github.io

## Project Overview
This is an **educational HTML tool suite** that generates interactive student games from teacher input. Teachers use standalone HTML files to configure questions/content, then download student-facing game files.

## Architecture Pattern

Each tool follows a two-phase architecture:
1. **Teacher Setup (Same File)**: Interactive form UI where teachers input content (questions, choices, words, etc.)
2. **Student Game Generator**: JavaScript embeds a complete HTML template string that gets downloaded with teacher data

**Key Insight**: The student game HTML is baked into the teacher file as a template literal. The `generate()` function:
- Collects teacher input via form
- Substitutes data into placeholders like `//%%DATA%%`, `//%%TITLE%%`
- Creates a blob and triggers download

## Tool Structure

| File | Purpose |
|------|---------|
| `Index.html` | Landing page with cards linking to all tools |
| `001` - Multiple Choice Maker | Teacher form → student multiple-choice quiz |
| `002` - Binary Choices | Configurable binary choice game with image upload |
| `003` - Word Guesser | Hangman-style word guessing game |
| `004` - Word Jumbler | Sentence word-reordering game |
| `005` - Fill in Blanks | Worksheet generator with answer key export |
| `006` - Multiple Choice w/ Images | Multiple choice with per-choice image support |

## Critical Patterns

### 1. Form Row Management
All tools use dynamic row containers. Pattern:
```javascript
const container = document.getElementById('rowsContainer');

function addRow() {
    rowCount++;
    const div = document.createElement('div');
    div.className = 'row';
    div.innerHTML = `...form inputs...`;
    container.appendChild(div);
}

function autoAdd(input) {
    // Auto-create new row when last row is filled
    if (input.parentElement === container.lastElementChild && input.value.trim() !== "") {
        addRow();
    }
}

function renumber() {
    [...container.children].forEach((row, i) => row.firstElementChild.textContent = i + 1);
}
```

### 2. Data Collection Pattern
Before generation, always iterate container children and filter empty rows:
```javascript
const data = [];
[...container.children].forEach(row => {
    const ins = row.querySelectorAll('input');
    if(ins[0].value.trim()) {  // Only non-empty entries
        data.push({/* structured data */});
    }
});
```

### 3. Template Download Pattern
```javascript
const finalHTML = studentTemplate
    .replace('//%%TITLE%%', `const gameTitle = "${title}";`)
    .replace('//%%DATA%%', `const gameData = ${JSON.stringify(data)};`);

const blob = new Blob([finalHTML], {type: 'text/html'});
const a = document.createElement('a');
a.href = URL.createObjectURL(blob);
a.download = title.replace(/\s+/g, '_') + ".html";
a.click();
```

### 4. Student Game UI Standards
All student games include:
- **5-level zoom** (scale-1 to scale-5): `body.scale-1 { font-size: 30px; }`
- **Fixed bottom navigation bar**: `#bottomBar` with nav buttons
- **Floating zoom button**: Fixed position FAB (Floating Action Button)
- **Screen switching**: `.screen.active` to show/hide screens via `display: flex/none`
- **Watermark**: Opacity 0.3 for teacher credit

**Intro Screen Pattern**:
```html
<div id="introScreen" class="screen active" style="background: #003366; color: white;">
    <!-- Large title, start button -->
</div>
```

### 5. UI/Style Consistency
- **Colors**: Primary `#003366` (navy), Secondary `#607d8b` (slate), Danger `#c62828` (red)
- **Teacher sections**: `background: #f8f9fa; padding: 15px; border-radius: 10px; border: 1px solid #eee`
- **Buttons**: `border-radius: 8px; padding: 12px 24px;`
- **Row grids**: Use CSS Grid with gap for clean alignment

## Common Gotchas

1. **Image Upload**: Always use `FileReader` + `readAsDataURL()` for preview before generation
2. **Data Serialization**: Use `JSON.stringify()` for embedding arrays/objects in template string
3. **File Naming**: Replace spaces with underscores: `title.replace(/\s+/g, '_')`
4. **Dynamic Row Numbering**: Call `renumber()` after deletion to maintain sequence
5. **Template Escaping**: Use backticks and `${...}` syntax to avoid quote conflicts

## Adding a New Tool

1. Create new HTML file (number in sequence)
2. Copy teacher form structure from similar tool (e.g., 001 for multiple choice)
3. Embed student game template as `const studentTemplate = \`...\``
4. Implement `generate()` and data collection in teacher form
5. Add card link to `Index.html` with matching numbering
6. Test download + student game interactivity

## Tech Stack
- **Framework**: None (vanilla HTML/CSS/JS)
- **Deployment**: GitHub Pages (static files)
- **Export Format**: Self-contained HTML (no external dependencies)

## Watermark Convention
Each tool includes a watermark (opacity: 0.3) visible only in game mode. Check the specific file for creator attribution (e.g., "cmarasigan" in tool 005).
