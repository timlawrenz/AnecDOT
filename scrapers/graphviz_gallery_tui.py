"""Textual TUI for Graphviz Gallery scraper.

Provides an interactive terminal UI with live progress, statistics,
and log viewing for better user experience during scraping.
"""

import asyncio
from datetime import datetime
from textual.app import App, ComposeResult
from textual.containers import Container, Vertical, Horizontal
from textual.widgets import Header, Footer, Static, ProgressBar, Log, Button
from textual.reactive import reactive
from textual import work

from scrapers.graphviz_gallery import GraphvizGalleryScraper


class StatsDisplay(Static):
    """Display scraper statistics in real-time."""
    
    total_found = reactive(0)
    total_scraped = reactive(0)
    validation_passed = reactive(0)
    validation_failed = reactive(0)
    duplicates_skipped = reactive(0)
    examples_written = reactive(0)
    pass_rate = reactive(0.0)
    
    def render(self) -> str:
        """Render statistics display."""
        return f"""[bold]Scraper Statistics[/bold]

📊 Examples found:      {self.total_found}
📝 Examples scraped:    {self.total_scraped}
✅ Validation passed:   {self.validation_passed}
❌ Validation failed:   {self.validation_failed}
📈 Pass rate:           {self.pass_rate:.1f}%
🔁 Duplicates skipped:  {self.duplicates_skipped}
💾 Examples written:    {self.examples_written}
"""


class ScraperTUI(App):
    """Textual TUI for Graphviz Gallery scraper."""
    
    CSS = """
    Screen {
        background: $surface;
    }
    
    #stats-container {
        width: 40;
        height: 100%;
        border: solid $primary;
        margin: 1;
    }
    
    #main-container {
        height: 100%;
    }
    
    #log-container {
        height: 100%;
        border: solid $accent;
        margin: 1;
    }
    
    #progress-container {
        height: 5;
        border: solid $secondary;
        margin: 1;
    }
    
    #controls {
        height: auto;
        margin: 1;
    }
    
    Button {
        margin: 0 1;
    }
    """
    
    BINDINGS = [
        ("q", "quit", "Quit"),
        ("p", "pause", "Pause/Resume"),
        ("s", "stop", "Stop"),
    ]
    
    def __init__(self, output_path: str = "./data/documentation-stream.jsonl", **kwargs):
        super().__init__()
        self.output_path = output_path
        self.scraper_kwargs = kwargs
        self.scraper = None
        self.is_paused = False
        self.is_stopped = False
    
    def compose(self) -> ComposeResult:
        """Create child widgets."""
        yield Header()
        
        with Horizontal(id="main-container"):
            # Left side: Statistics
            with Vertical(id="stats-container"):
                yield StatsDisplay(id="stats")
            
            # Right side: Progress and logs
            with Vertical():
                # Progress bar
                with Container(id="progress-container"):
                    yield Static("[bold]Scraping Progress[/bold]\n")
                    yield ProgressBar(total=100, show_eta=True, id="progress")
                    yield Static("", id="status")
                
                # Controls
                with Horizontal(id="controls"):
                    yield Button("Start", id="start-btn", variant="success")
                    yield Button("Pause", id="pause-btn", variant="warning", disabled=True)
                    yield Button("Stop", id="stop-btn", variant="error", disabled=True)
                
                # Log viewer
                with Container(id="log-container"):
                    yield Static("[bold]Activity Log[/bold]")
                    yield Log(id="log", auto_scroll=True)
        
        yield Footer()
    
    def on_mount(self) -> None:
        """Handle app mount."""
        self.title = "AnecDOT - Graphviz Gallery Scraper"
        log = self.query_one("#log", Log)
        log.write_line("🚀 Scraper ready. Click 'Start' to begin.")
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        button_id = event.button.id
        
        if button_id == "start-btn":
            self.start_scraping()
        elif button_id == "pause-btn":
            self.toggle_pause()
        elif button_id == "stop-btn":
            self.stop_scraping()
    
    def start_scraping(self) -> None:
        """Start the scraping process."""
        # Disable start, enable pause/stop
        self.query_one("#start-btn", Button).disabled = True
        self.query_one("#pause-btn", Button).disabled = False
        self.query_one("#stop-btn", Button).disabled = False
        
        log = self.query_one("#log", Log)
        log.write_line("✓ Starting scraper...")
        log.write_line(f"Output: {self.output_path}")
        
        # Run scraper in background
        self.run_scraper_async()
    
    def toggle_pause(self) -> None:
        """Pause/resume scraping."""
        self.is_paused = not self.is_paused
        pause_btn = self.query_one("#pause-btn", Button)
        log = self.query_one("#log", Log)
        
        if self.is_paused:
            pause_btn.label = "Resume"
            log.write_line("⏸ Paused")
        else:
            pause_btn.label = "Pause"
            log.write_line("▶ Resumed")
    
    def stop_scraping(self) -> None:
        """Stop the scraping process."""
        self.is_stopped = True
        log = self.query_one("#log", Log)
        log.write_line("⏹ Stopping scraper...")
        
        # Disable controls
        self.query_one("#pause-btn", Button).disabled = True
        self.query_one("#stop-btn", Button).disabled = True
    
    @work(exclusive=True)
    async def run_scraper_async(self) -> None:
        """Run scraper in background worker."""
        log = self.query_one("#log", Log)
        stats_widget = self.query_one("#stats", StatsDisplay)
        progress = self.query_one("#progress", ProgressBar)
        status = self.query_one("#status", Static)
        
        try:
            # Create scraper with custom logger that writes to TUI
            scraper = GraphvizGalleryScraper(
                output_path=self.output_path,
                **self.scraper_kwargs
            )
            
            # Fetch gallery index
            log.write_line("📡 Fetching gallery index...")
            from scrapers.graphviz_gallery import GALLERY_URL
            index_html = scraper._fetch_url(GALLERY_URL)
            
            if not index_html:
                log.write_line("❌ Failed to fetch gallery index")
                return
            
            # Extract example links
            example_urls = scraper.extract_example_links(index_html)
            total = len(example_urls)
            
            stats_widget.total_found = total
            progress.total = total
            log.write_line(f"✓ Found {total} example pages")
            
            # Process each example
            for idx, url in enumerate(example_urls, 1):
                # Check for stop/pause
                while self.is_paused and not self.is_stopped:
                    await asyncio.sleep(0.1)
                
                if self.is_stopped:
                    log.write_line("⚠ Scraping stopped by user")
                    break
                
                # Update status
                status.update(f"Processing {idx}/{total}: {url[:60]}...")
                log.write_line(f"📄 {idx}/{total}: {url}")
                
                # Fetch and process
                html = scraper._fetch_url(url)
                if html:
                    examples = scraper.extract_example_content(url, html)
                    stats_widget.total_scraped += len(examples)
                    
                    for example in examples:
                        scraper._process_example(example)
                        
                        # Update stats from scraper metrics
                        stats_widget.validation_passed = scraper.metrics.validation_passed
                        stats_widget.validation_failed = scraper.metrics.validation_failed
                        stats_widget.duplicates_skipped = scraper.metrics.duplicates_skipped
                        stats_widget.examples_written = scraper.metrics.examples_written
                        
                        # Calculate pass rate
                        total_validated = scraper.metrics.validation_passed + scraper.metrics.validation_failed
                        if total_validated > 0:
                            stats_widget.pass_rate = (scraper.metrics.validation_passed / total_validated) * 100
                
                # Update progress
                progress.advance(1)
                
                # Rate limiting
                if idx < total:
                    await asyncio.sleep(scraper.delay)
            
            # Finish
            scraper.metrics.finish()
            log.write_line("\n✅ Scraping complete!")
            log.write_line(scraper.metrics.summary())
            
            # Re-enable start button
            self.query_one("#start-btn", Button).disabled = False
            self.query_one("#pause-btn", Button).disabled = True
            self.query_one("#stop-btn", Button).disabled = True
            
        except Exception as e:
            log.write_line(f"❌ Error: {str(e)}")
            import traceback
            log.write_line(traceback.format_exc())
    
    def action_pause(self) -> None:
        """Pause/resume via keybinding."""
        if not self.query_one("#pause-btn", Button).disabled:
            self.toggle_pause()
    
    def action_stop(self) -> None:
        """Stop via keybinding."""
        if not self.query_one("#stop-btn", Button).disabled:
            self.stop_scraping()


def main():
    """Run the TUI application."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Graphviz Gallery Scraper - Textual TUI"
    )
    parser.add_argument(
        '--output',
        default='./data/documentation-stream.jsonl',
        help='Output JSONL file path'
    )
    parser.add_argument(
        '--delay',
        type=float,
        default=1.0,
        help='Delay between requests in seconds'
    )
    parser.add_argument(
        '--retries',
        type=int,
        default=3,
        help='Number of retries for failed requests'
    )
    
    args = parser.parse_args()
    
    app = ScraperTUI(
        output_path=args.output,
        delay=args.delay,
        retries=args.retries
    )
    app.run()


if __name__ == '__main__':
    main()
