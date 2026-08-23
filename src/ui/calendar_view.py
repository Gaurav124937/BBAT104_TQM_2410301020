from __future__ import annotations

import calendar
from datetime import date

import customtkinter as ctk

from services.calendar_service import get_month_events, get_upcoming_due


class CalendarView(ctk.CTkFrame):
    """
    Clean responsive Library Activity Calendar.

    Design:
    - No forced horizontal width.
    - Entire calendar page is vertically scrollable.
    - The 7-column calendar always fits the available width.
    - Every date cell is selectable as a whole.
    - Issue/Due/Return activity is shown compactly inside each date.
    - Details and upcoming due dates are shown below the calendar.
    """

    def __init__(self, master):
        super().__init__(master, fg_color="transparent")

        today = date.today()
        self.year = today.year
        self.month = today.month
        self.selected_day = today.day
        self.events: dict[int, list[dict]] = {}

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._build_scroll_container()
        self._build_header()
        self._build_calendar()
        self._build_details()

        self.refresh()

    # ------------------------------------------------------------------
    # Scroll container
    # ------------------------------------------------------------------

    def _build_scroll_container(self) -> None:
        self.page = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
        )
        self.page.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=0,
            pady=0,
        )

        self.page.grid_columnconfigure(0, weight=1)

    # ------------------------------------------------------------------
    # Header
    # ------------------------------------------------------------------

    def _build_header(self) -> None:
        header = ctk.CTkFrame(
            self.page,
            fg_color="transparent",
        )
        header.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=20,
            pady=(16, 10),
        )
        header.grid_columnconfigure(2, weight=1)

        ctk.CTkButton(
            header,
            text="‹",
            width=42,
            command=self.previous_month,
        ).grid(
            row=0,
            column=0,
            padx=(0, 6),
        )

        ctk.CTkButton(
            header,
            text="Today",
            width=78,
            command=self.go_today,
        ).grid(
            row=0,
            column=1,
        )

        title_box = ctk.CTkFrame(
            header,
            fg_color="transparent",
        )
        title_box.grid(
            row=0,
            column=2,
        )

        self.month_label = ctk.CTkLabel(
            title_box,
            text="",
            font=ctk.CTkFont(
                size=27,
                weight="bold",
            ),
        )
        self.month_label.pack()

        ctk.CTkLabel(
            title_box,
            text="Library Activity Calendar",
            font=ctk.CTkFont(size=12),
        ).pack(
            pady=(1, 0),
        )

        ctk.CTkButton(
            header,
            text="›",
            width=42,
            command=self.next_month,
        ).grid(
            row=0,
            column=3,
            padx=(6, 0),
        )

    # ------------------------------------------------------------------
    # Calendar
    # ------------------------------------------------------------------

    def _build_calendar(self) -> None:
        panel = ctk.CTkFrame(
            self.page,
            corner_radius=12,
        )
        panel.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=20,
            pady=(0, 10),
        )

        panel.grid_columnconfigure(
            tuple(range(7)),
            weight=1,
            uniform="calendar_columns",
        )

        # Legend
        legend = ctk.CTkFrame(
            panel,
            fg_color="transparent",
        )
        legend.grid(
            row=0,
            column=0,
            columnspan=7,
            sticky="ew",
            padx=12,
            pady=(10, 6),
        )

        for symbol, label in (
            ("I", "Issue"),
            ("D", "Due"),
            ("R", "Return"),
        ):
            item = ctk.CTkFrame(
                legend,
                fg_color="transparent",
            )
            item.pack(
                side="left",
                padx=(0, 16),
            )

            ctk.CTkLabel(
                item,
                text=symbol,
                width=22,
                height=22,
                corner_radius=6,
                font=ctk.CTkFont(
                    size=10,
                    weight="bold",
                ),
            ).pack(side="left")

            ctk.CTkLabel(
                item,
                text=label,
                font=ctk.CTkFont(size=12),
            ).pack(
                side="left",
                padx=(4, 0),
            )

        # Weekday header
        for col, weekday in enumerate(
            ("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun")
        ):
            ctk.CTkLabel(
                panel,
                text=weekday,
                font=ctk.CTkFont(
                    size=12,
                    weight="bold",
                ),
            ).grid(
                row=1,
                column=col,
                sticky="ew",
                padx=3,
                pady=(0, 6),
            )

        self.calendar_grid = ctk.CTkFrame(
            panel,
            fg_color="transparent",
        )
        self.calendar_grid.grid(
            row=2,
            column=0,
            columnspan=7,
            sticky="ew",
            padx=6,
            pady=(0, 8),
        )

        self.calendar_grid.grid_columnconfigure(
            tuple(range(7)),
            weight=1,
            uniform="day_columns",
        )

    def _render_calendar(self) -> None:
        for widget in self.calendar_grid.winfo_children():
            widget.destroy()

        weeks = calendar.Calendar(
            firstweekday=0,
        ).monthdayscalendar(
            self.year,
            self.month,
        )

        today = date.today()

        for row_index, week in enumerate(weeks):
            self.calendar_grid.grid_rowconfigure(
                row_index,
                weight=1,
                minsize=78,
            )

            for col_index, day in enumerate(week):
                if day == 0:
                    ctk.CTkFrame(
                        self.calendar_grid,
                        fg_color="transparent",
                    ).grid(
                        row=row_index,
                        column=col_index,
                        sticky="nsew",
                        padx=3,
                        pady=3,
                    )
                    continue

                event_list = self.events.get(day, [])

                is_today = (
                    today.year == self.year
                    and today.month == self.month
                    and today.day == day
                )

                is_selected = day == self.selected_day

                # Entire cell is the selectable target.
                cell = ctk.CTkFrame(
                    self.calendar_grid,
                    corner_radius=10,
                    border_width=2 if is_selected else 1,
                )
                cell.grid(
                    row=row_index,
                    column=col_index,
                    sticky="nsew",
                    padx=3,
                    pady=3,
                )

                # Header text.
                ctk.CTkLabel(
                    cell,
                    text=(
                        f"{day}"
                        f"{' • Today' if is_today else ''}"
                    ),
                    anchor="w",
                    font=ctk.CTkFont(
                        size=11,
                        weight=(
                            "bold"
                            if (is_today or is_selected)
                            else "normal"
                        ),
                    ),
                ).pack(
                    fill="x",
                    padx=8,
                    pady=(7, 4),
                )

                if event_list:
                    counts = {
                        "Issue": sum(
                            event["type"] == "Issue"
                            for event in event_list
                        ),
                        "Due": sum(
                            event["type"] == "Due"
                            for event in event_list
                        ),
                        "Return": sum(
                            event["type"] == "Return"
                            for event in event_list
                        ),
                    }

                    for event_type in (
                        "Issue",
                        "Due",
                        "Return",
                    ):
                        count = counts[event_type]
                        if count:
                            ctk.CTkLabel(
                                cell,
                                text=(
                                    f"{self._symbol(event_type)}"
                                    f"  {count}"
                                ),
                                anchor="w",
                                font=ctk.CTkFont(
                                    size=11,
                                    weight="bold",
                                ),
                            ).pack(
                                fill="x",
                                padx=8,
                                pady=2,
                            )
                else:
                    ctk.CTkLabel(
                        cell,
                        text="",
                    ).pack(
                        fill="both",
                        expand=True,
                    )

                # Make the COMPLETE date card clickable.
                self._bind_whole_cell(
                    cell,
                    day,
                )

    def _bind_whole_cell(self, widget, day: int) -> None:
        try:
            widget.configure(cursor="hand2")
        except Exception:
            pass

        widget.bind(
            "<Button-1>",
            lambda _event, selected_day=day: self.select_day(
                selected_day
            ),
        )

        for child in widget.winfo_children():
            self._bind_whole_cell(
                child,
                day,
            )

    @staticmethod
    def _symbol(event_type: str) -> str:
        return {
            "Issue": "I",
            "Due": "D",
            "Return": "R",
        }[event_type]

    # ------------------------------------------------------------------
    # Details
    # ------------------------------------------------------------------

    def _build_details(self) -> None:
        panel = ctk.CTkFrame(
            self.page,
            corner_radius=12,
        )
        panel.grid(
            row=2,
            column=0,
            sticky="ew",
            padx=20,
            pady=(0, 16),
        )

        panel.grid_columnconfigure(
            1,
            weight=1,
            uniform="detail_columns",
        )
        panel.grid_columnconfigure(
            2,
            weight=1,
            uniform="detail_columns",
        )

        date_box = ctk.CTkFrame(
            panel,
            fg_color="transparent",
        )
        date_box.grid(
            row=0,
            column=0,
            sticky="nsw",
            padx=16,
            pady=16,
        )

        ctk.CTkLabel(
            date_box,
            text="Selected Date",
            font=ctk.CTkFont(
                size=16,
                weight="bold",
            ),
        ).pack(
            anchor="w",
        )

        self.selected_label = ctk.CTkLabel(
            date_box,
            text="",
            font=ctk.CTkFont(size=13),
        )
        self.selected_label.pack(
            anchor="w",
            pady=(4, 8),
        )

        self.summary = ctk.CTkLabel(
            date_box,
            text="",
            justify="left",
            anchor="w",
        )
        self.summary.pack(
            anchor="w",
        )

        ctk.CTkLabel(
            panel,
            text="Activity Details",
            font=ctk.CTkFont(
                size=14,
                weight="bold",
            ),
        ).grid(
            row=0,
            column=1,
            sticky="nw",
            padx=14,
            pady=(12, 0),
        )

        self.details_box = ctk.CTkScrollableFrame(
            panel,
            height=170,
            fg_color="transparent",
        )
        self.details_box.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=10,
            pady=(34, 10),
        )

        ctk.CTkLabel(
            panel,
            text="Upcoming Due Dates",
            font=ctk.CTkFont(
                size=14,
                weight="bold",
            ),
        ).grid(
            row=0,
            column=2,
            sticky="nw",
            padx=14,
            pady=(12, 0),
        )

        self.upcoming_box = ctk.CTkScrollableFrame(
            panel,
            height=170,
            fg_color="transparent",
        )
        self.upcoming_box.grid(
            row=0,
            column=2,
            sticky="nsew",
            padx=(10, 16),
            pady=(34, 10),
        )

    def _show_details(self) -> None:
        selected = date(
            self.year,
            self.month,
            self.selected_day,
        )

        self.selected_label.configure(
            text=selected.strftime(
                "%A, %d %B %Y"
            ),
        )

        for widget in self.details_box.winfo_children():
            widget.destroy()

        event_list = self.events.get(
            self.selected_day,
            [],
        )

        counts = {
            "Issue": 0,
            "Due": 0,
            "Return": 0,
        }

        if not event_list:
            ctk.CTkLabel(
                self.details_box,
                text="No activity on this date.",
            ).pack(
                anchor="w",
                padx=8,
                pady=12,
            )
        else:
            for event in event_list:
                counts[event["type"]] += 1

                card = ctk.CTkFrame(
                    self.details_box,
                    corner_radius=8,
                )
                card.pack(
                    fill="x",
                    padx=4,
                    pady=4,
                )

                ctk.CTkLabel(
                    card,
                    text=(
                        f'{event["type"]}'
                        f' • {event["title"]}'
                    ),
                    anchor="w",
                    wraplength=360,
                    font=ctk.CTkFont(
                        size=12,
                        weight="bold",
                    ),
                ).pack(
                    fill="x",
                    padx=10,
                    pady=(8, 2),
                )

                ctk.CTkLabel(
                    card,
                    text=event["details"],
                    anchor="w",
                    wraplength=360,
                    font=ctk.CTkFont(size=11),
                ).pack(
                    fill="x",
                    padx=10,
                    pady=(0, 8),
                )

        self.summary.configure(
            text=(
                f'Issues: {counts["Issue"]}\n'
                f'Due: {counts["Due"]}\n'
                f'Returns: {counts["Return"]}'
            ),
        )

        for widget in self.upcoming_box.winfo_children():
            widget.destroy()

        upcoming = get_upcoming_due(7)

        if not upcoming:
            ctk.CTkLabel(
                self.upcoming_box,
                text="No due dates in the next 7 days.",
            ).pack(
                anchor="w",
                padx=8,
                pady=12,
            )
        else:
            for row in upcoming:
                ctk.CTkLabel(
                    self.upcoming_box,
                    text=(
                        f'{row["due_date"]}'
                        f' • {row["title"]}\n'
                        f'{row["member_name"]}'
                    ),
                    justify="left",
                    anchor="w",
                ).pack(
                    fill="x",
                    padx=8,
                    pady=4,
                )

    # ------------------------------------------------------------------
    # Navigation
    # ------------------------------------------------------------------

    def refresh(self) -> None:
        self.events = get_month_events(
            self.year,
            self.month,
        )

        self.month_label.configure(
            text=date(
                self.year,
                self.month,
                1,
            ).strftime("%B %Y"),
        )

        self._render_calendar()
        self._show_details()

    def select_day(self, day: int) -> None:
        self.selected_day = day
        self._render_calendar()
        self._show_details()

    def previous_month(self) -> None:
        if self.month == 1:
            self.year -= 1
            self.month = 12
        else:
            self.month -= 1

        self.selected_day = 1
        self.refresh()

    def next_month(self) -> None:
        if self.month == 12:
            self.year += 1
            self.month = 1
        else:
            self.month += 1

        self.selected_day = 1
        self.refresh()

    def go_today(self) -> None:
        today = date.today()
        self.year = today.year
        self.month = today.month
        self.selected_day = today.day
        self.refresh()
