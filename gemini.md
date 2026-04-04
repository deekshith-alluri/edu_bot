## Core Objective

Generate ONLY frontend UI (HTML/CSS/JS) for the project.

## Hard Restrictions 

* DO NOT modify, access, or generate backend code
* DO NOT create APIs, database logic, or server-side code
* DO NOT assume backend structure
* ONLY create UI files

## Allowed Technologies

* HTML5
* CSS3
* Tailwind CSS / Bootstrap (either or mix allowed)
* Vanilla JavaScript ONLY (no frameworks)

---

## Required Pages

Create the following files:

* welcome.html
* authenticate.html
* profile.html
* dashboard.html
* base.html (shared layout if needed)

Use a **consistent, modern, attractive color theme** across all pages.

---

# welcome.html

## Navbar

* Left: [Login] [Get Started]
* Right: "Study Spark" (logo/name)

## Body

* Beautiful landing page
* Sections explaining services
* Use:

  * Attractive layouts
  * Cards / grids
  * Clean typography
  * Relevant images

---

# authenticate.html

## Dual Mode UI

* Login form
* Register form (toggle based on button clicked)

## Login Form

* Username
* Password

## Register Flow (IMPORTANT)

1. First ask for username
2. Validate (simulate UI only):

   * If taken → show error
   * If available → show full form

## Register Form Fields

* Password
* First Name
* Last Name
* Class of Study
* Date of Birth
* Country
* State
* School
* Board of Education
* Phone Number
* Email

---

# profile.html

## Navbar

* Left: Study Spark
* Right: [Edit Profile] [Dashboard] [Delete Account] [Logout]

## Body

* Display user data 
when edit profile is clicked :
* Editable fields
* Update functionality (UI only)

---

# dashboard.html (CRITICAL SECTION)

## Device Restriction

* If screen is small → show animation:
  "Dashboard not available on small screens"

---

## Navbar

* Left: Study Spark
* Right: [Profile] [Logout]

---

## Chat UI

* ChatGPT-like interface
* Input box:

  * Auto-growing textarea
  * ENTER = send
* Icons:

  * [+] Attachment
  * [Paper Plane Icon] Send button

## Chat Behavior

* Sent messages → Right
* Received messages → Left

---

## File Upload Rules

* Only PDF allowed
* Max size: 10MB
* If >10MB → show alert and terminate

## Attachment Popup

On clicking [+]:

* Show floating panel:
  "Only written PDFs up to 10MB are supported"
* Upload button

---

## PDF Mode

After upload:

* Add navbar button: [Open PDF]
* Clicking:

  * Split screen into 2 columns

    * Left: Chat
    * Right: PDF Viewer
* Toggle:

  * Open PDF (Item) ↔ [X] on left of the respective column

---

## Response Handling Logic (VERY IMPORTANT)

### Backend Response Format

```
{
  query,
  classification: { classified_into },
  simple_explanation,
  deep_explanation,
  quiz,
  youtube_recommendations
}
```

---

## CASE 1: SIMPLE / FACT-CHECK

* Stay in chat mode
* Extract from simple_explanation.answer
* Remove <html> tags
* Display as chat message

---

## CASE 2: MEDIUM

* Use deep_explanation
* Remove HTML tags
* Show in chat

---

## CASE 3: HARD (MAJOR LAYOUT SHIFT)

### Layout Split

* Screen splits into 2 resizable panels

### Right Side

* Chat UI (compressed)

### Left Side

1. YouTube row

   * Horizontal scroll
   * Infinite loop feel

2. Quiz Section

   * Build interactive MCQs
   * Highlight correct answers

### Controls

* Close button for this panel
* Open [Item] in the nav bar <-> [X] on left of the respective column

---

## ADVANCED INTERACTION RULES

### If PDF is OPEN + HARD classification

* Add navbar button: [Open Quiz]
* On click:

  * Close PDF
  * Open quiz + YouTube panel

---

## Dynamic Navbar Buttons

* Open PDF
* [X]
* Open Quiz

---

## Close Icons

Each panel has [X]

* Closing restores layout
* Adds "Open [Item]" back to navbar

---

## Animations & UX

* Smooth transitions
* Use transforms for layout shifts
* Resizable panels (mouse drag)

---

## base.html

* Shared layout structure
* Common navbar/footer styles

---

## Final Expectations

* Clean UI
* Fully responsive (except dashboard restriction)
* Smooth UX
* Modular code

---

## ABSOLUTE RULE

If any instruction conflicts:
PRIORITIZE UI-ONLY GENERATION
NEVER TOUCH BACKEND

