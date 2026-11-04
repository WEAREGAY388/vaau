import sys
import os
import requests
import threading
import gi

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, GLib, GdkPixbuf, Gio

from catgirl_downloader.sources.manager import SourceManager

class CatgirlDownloaderApp(Adw.Application):
    def __init__(self):
        super().__init__(application_id="io.github.catgirldownloader",
                         flags=Gio.ApplicationFlags.FLAGS_NONE)

    def do_activate(self):
        win = MainWindow(application=self)
        win.present()

class MainWindow(Adw.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_title("Catgirl Downloader")
        self.set_default_size(900, 650)
        
        self.manager = SourceManager()
        
        # Main layout container
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.set_content(main_box)
        
        # Header bar
        header = Adw.HeaderBar()
        main_box.append(header)
        
        # Controls Bar
        controls_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        controls_box.set_margin_start(12)
        controls_box.set_margin_end(12)
        controls_box.set_margin_top(10)
        controls_box.set_margin_bottom(10)
        
        # Source dropdown
        self.source_combo = Gtk.DropDown.new_from_strings(self.manager.list_sources())
        controls_box.append(self.source_combo)
        
        # Tag entry
        self.tag_entry = Gtk.Entry()
        self.tag_entry.set_placeholder_text("Enter tags (e.g., rating:s cat_ears)...")
        self.tag_entry.set_hexpand(True)
        controls_box.append(self.tag_entry)
        
        # Limit spin button
        self.limit_spin = Gtk.SpinButton.new_with_range(1, 50, 1)
        self.limit_spin.set_value(10)
        controls_box.append(self.limit_spin)
        
        # Search Button
        search_btn = Gtk.Button(label="Fetch Images")
        search_btn.add_css_class("suggested-action")
        search_btn.connect("clicked", self.on_search_clicked)
        controls_box.append(search_btn)
        
        main_box.append(controls_box)
        
        # Scrolled FlowBox for image gallery
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_vexpand(True)
        main_box.append(scrolled)
        
        self.flowbox = Gtk.FlowBox()
        self.flowbox.set_valign(Gtk.Align.START)
        self.flowbox.set_max_children_per_line(4)
        self.flowbox.set_selection_mode(Gtk.SelectionMode.NONE)
        self.flowbox.set_margin_start(12)
        self.flowbox.set_margin_end(12)
        self.flowbox.set_margin_top(12)
        self.flowbox.set_margin_bottom(12)
        scrolled.set_child(self.flowbox)

    def on_search_clicked(self, widget):
        selected_idx = self.source_combo.get_selected()
        sources_list = self.manager.list_sources()
        if selected_idx >= len(sources_list):
            return
        
        source_name = sources_list[selected_idx]
        tags = self.tag_entry.get_text().strip()
        limit = int(self.limit_spin.get_value())
        
        # Clear existing flowbox items
        while child := self.flowbox.get_first_child():
            self.flowbox.remove(child)
            
        # Run fetch in background thread to keep UI responsive
        threading.Thread(target=self.fetch_and_populate, args=(source_name, tags, limit), daemon=True).start()

    def fetch_and_populate(self, source_name, tags, limit):
        source = self.manager.get_source(source_name)
        if not source:
            return
        
        posts = source.fetch_images(tags=tags, limit=limit)
        GLib.idle_add(self.render_posts, posts)

    def render_posts(self, posts):
        for post in posts:
            card = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
            card.set_size_request(200, 240)
            card.add_css_class("card")
            
            label = Gtk.Label(label=f"[{post['source']}] #{post['id']}")
            label.set_ellipsize(3) # PANGO_ELLIPSIZE_END
            card.append(label)
            
            # Action button to download full image
            btn = Gtk.Button(label="Open Image Link")
            btn.connect("clicked", lambda b, url=post['image_url']: Gio.AppInfo.launch_default_for_uri(url, None))
            card.append(btn)
            
            self.flowbox.append(card)

def main():
    app = CatgirlDownloaderApp()
    return app.run(sys.argv)

if __name__ == "__main__":
    main()
