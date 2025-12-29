export function Footer() {
  return (
    <footer className="w-full px-8 py-6 border-t border-border">
      <div className="container mx-auto flex items-center justify-between text-sm text-secondary-text">
        <p>&copy; {new Date().getFullYear()} Secure Todo. All Rights Reserved.</p>
        <div className="flex gap-4">
          <a href="#" className="hover:text-primary-text transition-colors">
            Privacy Policy
          </a>
          <a href="#" className="hover:text-primary-text transition-colors">
            Terms of Service
          </a>
        </div>
      </div>
    </footer>
  );
}
