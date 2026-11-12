# How this project was built

This page says who did what, so that a reader can judge the project for what it is.

## In short

LVGL MPY Studio was designed and directed by one person, Nunzio Raciti, and written for the
most part by AI coding agents working under his direction. It is not a hand-written code base
with an assistant's help, and it is not an unattended output either: it is an experiment in how
far one engineer can take a whole product by directing agents, and a statement of the method
used to keep the result under control.

## Who did what

**The author**

- chose what to build and in which order, and what to leave out;
- set the constraints: the targets, the pinned versions of MicroPython and LVGL, the licences,
  English as the language of the code, what may be published and when;
- decided between the alternatives the agents proposed, and rejected some;
- owns the hardware: boards, firmware, wiring, and the judgement of what is seen on a display;
- wrote the STM32H743 display and touch drivers himself, months before this project, and
  proposed them upstream; they were later ported to a repository of their own with the help
  of AI agents. [The stack](stack.md) has the links.

**The agents** (Claude Code, with Anthropic's Claude models)

- wrote most of the source code, the tests and the documentation;
- reviewed the code in dedicated passes, and fixed what the reviews found;
- ran the test suite, the simulator and, when asked, the boards attached to the author's computer;
- reported what they had not verified. That list is in [the status page](status.md).

Commits written this way carry a `Co-Authored-By` line naming the model. Nothing is hidden: of
the 162 commits of the first two weeks, 139 carry that line.

## The method

- **Decisions are written down** with their date and reason, in [decisions.md](decisions.md).
- **Every change comes with tests**: more than 1250 automated tests, among them pixel
  comparisons between the MicroPython and the C output of the same project.
- **The IDE tests itself**: `lvgl-mpy-studio selftest` drives the real window with mouse and
  keyboard through nine scenarios and reports each step. It found real defects that the unit
  tests had missed.
- **Agents do not publish.** Pushes, tags, releases and anything that touches a board need the
  author's explicit go-ahead.
- **Claims are separated from checks.** A feature is described as tried on a board only when
  it was; everything else is marked as not verified.

## What this method does not give

- **Human testing.** The suite is large, but few people have used the IDE. Much that is
  written and tested by machine has never been tried by a person on a real task. This is the
  main weakness of the project and it is stated plainly in [the status page](status.md).
- **Breadth before depth.** Features were added early when they were expected to be useful, so
  that the design would not have to be reopened later. The price is that several are complete
  on paper and thin in experience.
- **A long history to read.** See below.

## The history of the repository

Work started on 2026-10-28 under the name *LVGL IDE*. In two weeks it went through versions
0.1 to 0.4, a change of name, a change of the package and command names, the move from
Italian to English for code, comments and documents, and several experiments that were
dropped. That history has 162 commits, 18 branches and 21 pull requests.

On 2026-11-11, with version 0.5.0, the repository was started again from the state of the
sources at that moment, as a single first commit. The reason is tidiness, not concealment: the
old history mixed two names, two languages and discarded attempts, and was a poor base for
anyone joining the project.

What this means for a reader:

- the history visible here begins at 0.5.0; what came before cannot be inspected commit by commit;
- [the changelog](../CHANGELOG.md) lists what each version changed, from the first one;
- [decisions.md](decisions.md) keeps the dated decisions of the earlier period;
- the author keeps the earlier history.

The single first commit is therefore two weeks of work, not one day's.
