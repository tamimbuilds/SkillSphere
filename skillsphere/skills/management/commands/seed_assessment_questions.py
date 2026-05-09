from django.core.management.base import BaseCommand
from django.db import transaction
from skills.models import Skill, Question


class Command(BaseCommand):
    help = 'Seeds MCQ questions: 8 sectors, 3 sets, 10 questions each.'

    def handle(self, *args, **kwargs):
        # Format per entry: (question_text, opt_a, opt_b, opt_c, opt_d, correct)
        # 3 sets x 10 questions = 30 per sector
        SECTOR_QUESTIONS = {
            'frontend': [
                # SET 1
                ("What does the CSS Box Model consist of?", "Content, padding, border, margin", "Content and border only", "Padding and margin only", "Content only", "A"),
                ("Which HTML5 element defines navigation links?", "nav", "div", "section", "header", "A"),
                ("What does async/await handle in JavaScript?", "Asynchronous code in a readable way", "Blocking the event loop", "Replacing all callbacks permanently", "Preventing use of promises", "A"),
                ("What is CSS specificity?", "Priority system for applying CSS rules", "CSS file load ordering", "Count of CSS class names", "Range of CSS color values", "A"),
                ("What does localStorage do in the browser?", "Persists data with no expiration date", "Stores server-side sessions", "Manages HTTP cookies only", "Caches HTTP responses only", "A"),
                ("What is CSS Flexbox designed for?", "One-dimensional layout of items", "Two-dimensional grid layout", "CSS transition animations", "Database record layouts", "A"),
                ("What does 'use strict' enable in JavaScript?", "Strict mode that catches silent errors", "Disables all error handling", "Speeds up script execution", "Enables CSS parsing in JS", "A"),
                ("What is the viewport meta tag for?", "Controlling layout on mobile screens", "Setting the page background color", "Loading external JavaScript files", "Configuring server-side responses", "A"),
                ("What is CORS in web development?", "Policy governing cross-origin HTTP requests", "A special CSS property name", "A type of JavaScript function", "An HTML5 validation attribute", "A"),
                ("What does 'defer' on a script tag do?", "Loads script after HTML parsing completes", "Loads script before any HTML", "Completely disables JavaScript", "Minifies the script automatically", "A"),
                # SET 2
                ("What is JSX in React?", "JS syntax extension for writing HTML-like code", "A database query language", "A CSS preprocessor tool", "A React testing framework", "A"),
                ("What is a React hook?", "Function enabling state in functional components", "A class-based lifecycle method", "An HTML data attribute", "A CSS pseudo-class selector", "A"),
                ("What does useState return in React?", "A state variable and a setter function", "Only the current state value", "Only the state setter function", "A boolean flag value", "A"),
                ("What is Vue's v-bind directive used for?", "Binding reactive data to HTML attributes", "Looping through data arrays", "Handling user click events", "Defining child components", "A"),
                ("What is prop drilling in React?", "Passing data through many component layers", "A CSS gradient technique", "A webpack build optimization", "A React Router method", "A"),
                ("What does Vue's reactivity system do?", "Tracks data changes and updates the DOM", "Manages all HTTP API requests", "Handles CSS transition animations", "Runs server background jobs", "A"),
                ("What is React's key prop used for?", "Uniquely identifying items in a list", "Applying styles to list elements", "Binding click events to list items", "Animating list item transitions", "A"),
                ("What is a controlled component in React?", "Form element whose value React controls", "A self-managing DOM element", "A CSS-controlled element", "A server-side React component", "A"),
                ("What does Vue Router manage?", "Navigation between application pages", "All API data fetching logic", "Global application state", "Component rendering lifecycle", "A"),
                ("What is React Context API used for?", "Sharing state without prop drilling", "Replacing all CSS variables", "Running background API calls", "Optimizing bundle render speed", "A"),
                # SET 3
                ("What is Redux used for?", "Centralized application state management", "CSS keyframe animations", "Making HTTP API requests", "Running SQL database queries", "A"),
                ("What is code splitting in web apps?", "Loading JS bundles only when needed", "Splitting one CSS file into many", "Dividing HTML into sections", "Sharing code across repositories", "A"),
                ("What is lazy loading?", "Loading resources only when required", "Preloading all page assets upfront", "Caching all server responses", "A client-side routing technique", "A"),
                ("What does React.memo do?", "Skips re-render when props are unchanged", "Stores encrypted user passwords", "Logs all component render errors", "Compresses component image assets", "A"),
                ("What is Webpack?", "A JavaScript module bundler tool", "A utility CSS framework", "A React unit testing library", "A backend database ORM", "A"),
                ("What does useMemo do in React?", "Memoizes expensive computed values", "Fetches remote API data", "Handles form field submissions", "Manages page routing state", "A"),
                ("What is tree shaking in JavaScript?", "Removing unused code from the final bundle", "Building visual component trees", "Managing complex CSS selectors", "Compressing and optimizing images", "A"),
                ("What is hydration in SSR applications?", "Attaching JS interactivity to server HTML", "Loading CSS files on the client", "Fetching data from the database", "Compiling HTML template files", "A"),
                ("What is a service worker?", "Background script enabling caching and offline", "A reusable UI component type", "A CSS preprocessing tool", "A database connection driver", "A"),
                ("What does useCallback do in React?", "Returns a stable memoized callback function", "Fetches data from a remote API", "Manages component CSS class names", "Controls in-app page routing", "A"),
            ],
            'backend': [
                # SET 1
                ("What does REST stand for?", "Representational State Transfer", "Remote Execution Service Transfer", "Resource Encoding Standard Transfer", "Rapid Event Stream Technology", "A"),
                ("What HTTP status code means Not Found?", "404", "200", "500", "301", "A"),
                ("What is JWT used for?", "Stateless authentication via signed tokens", "Indexing database records faster", "Animating server-side CSS", "Caching HTTP request headers", "A"),
                ("What does HTTP POST do?", "Sends data to create a new resource", "Retrieves an existing resource", "Permanently deletes a resource", "Partially updates a resource", "A"),
                ("What is an API endpoint?", "A URL path where the API receives requests", "A database table structure definition", "A CSS selector property value", "A server-side error log entry", "A"),
                ("What is middleware in a web framework?", "Functions processing requests before route handlers", "Definitions of CSS stylesheets", "Database schema table definitions", "Frontend component UI definitions", "A"),
                ("What is the purpose of HTTP headers?", "Carry metadata about requests and responses", "Apply styling to web page elements", "Execute JavaScript on the server", "Render HTML content in browsers", "A"),
                ("What is API rate limiting?", "Restricting requests per client per time window", "Speeding up all API response times", "Caching database query results", "Encrypting all API response bodies", "A"),
                ("What does CRUD stand for?", "Create Read Update Delete", "Connect Render Update Deploy", "Cache Retrieve Unzip Delete", "Compile Run Update Debug", "A"),
                ("What is an ORM?", "Maps code objects to database tables", "A CSS grid layout system tool", "A JavaScript frontend test library", "An automated build pipeline tool", "A"),
                # SET 2
                ("What does database indexing do?", "Speeds up data retrieval query performance", "Automatically deletes old stale records", "Encrypts all stored table data", "Creates automatic database backups", "A"),
                ("What is the N+1 query problem?", "One extra DB query per related record in a loop", "Having only one database instance total", "Executing all queries in parallel threads", "Using no indexes on any table", "A"),
                ("What does SQL JOIN do?", "Combines rows from two or more tables", "Permanently deletes duplicate table rows", "Creates entirely new database tables", "Encrypts table column data at rest", "A"),
                ("What is a database transaction?", "An atomic set of operations: all succeed or all fail", "A single SQL SELECT retrieval query", "A relationship type between tables", "An automated database backup job", "A"),
                ("What is Redis commonly used for?", "In-memory caching and fast session storage", "Storing large binary file assets", "Server-side HTML template rendering", "Running machine learning model inference", "A"),
                ("What is database normalization?", "Organizing data to eliminate redundancy", "Encrypting the entire database schema", "Adding composite indexes to all tables", "Increasing the maximum table row size", "A"),
                ("What is a foreign key?", "Column referencing another table's primary key", "The very first column in every table", "An encrypted and hashed data column", "A temporary computed virtual column", "A"),
                ("What is database connection pooling?", "Reusing open DB connections to boost performance", "Creating automated database backup jobs", "Encrypting all database network connections", "Sharing one database across many servers", "A"),
                ("What is a database migration?", "Applying version-controlled schema changes to the DB", "Copying production data to another server", "Restoring a database from a backup file", "Exporting all table data to CSV format", "A"),
                ("What is a NoSQL database?", "Non-relational DB with a flexible schema", "A SQL database that has no indexes", "A faster drop-in PostgreSQL replacement", "A database exclusively for graph data", "A"),
                # SET 3
                ("What is SQL injection?", "Inserting malicious SQL through user inputs", "A common CSS rendering vulnerability", "A JavaScript runtime execution error", "A backend network connection timeout", "A"),
                ("How should user passwords be stored?", "Hashed using bcrypt or Argon2 algorithms", "Stored as reversible MD5 hash strings", "Stored as readable plain text strings", "Encoded using standard base64 encoding", "A"),
                ("What is HTTPS?", "HTTP secured with TLS/SSL encryption", "A significantly faster version of HTTP", "HTTP protocol designed for mobile devices", "HTTP protocol that omits request headers", "A"),
                ("What is a Cross-Site Scripting (XSS) attack?", "Injecting malicious scripts into web pages", "A CSS animation rendering glitch", "A critical server memory crash error", "A database connection refused error", "A"),
                ("Where should API secrets and keys be stored?", "In environment variables outside source code", "Committed to git for easy team sharing", "Hardcoded directly inside source code files", "Shared with teammates via plain email", "A"),
                ("What does horizontal scaling mean?", "Adding more server instances to handle load", "Upgrading the existing server's hardware", "Installing more RAM on the current server", "Increasing CPU core count on one machine", "A"),
                ("What is a CDN primarily used for?", "Delivering assets from servers near the user", "Storing and managing database backup files", "Running server-side application business logic", "Managing all user authentication sessions", "A"),
                ("What is load balancing?", "Distributing incoming traffic across multiple servers", "Continuously monitoring server error log files", "Scheduling automatic database backup tasks", "Encrypting all inbound and outbound traffic", "A"),
                ("What is CSRF protection?", "Preventing unauthorized cross-site form submissions", "Blocking all CSS-based styling attacks", "Filtering out SQL injection attack strings", "Disabling all browser cookie storage", "A"),
                ("What is database query optimization?", "Writing efficient queries that leverage indexes", "Adding as many database tables as possible", "Removing all existing database index files", "Rewriting all queries using only raw SQL", "A"),
            ],
            'fullstack': [
                # SET 1
                ("What is monolithic architecture?", "All components in a single deployable unit", "Separate microservices per feature", "Frontend-only codebase structure", "Backend-only codebase structure", "A"),
                ("What is microservices architecture?", "Small independent services communicating via APIs", "One large unified server application", "A CSS modular design methodology", "A database horizontal partitioning strategy", "A"),
                ("What is the MVC pattern?", "Model View Controller separation of concerns", "Model Version Control repository system", "Machine Vision Compiler framework", "Multi-Value Cache storage system", "A"),
                ("What is an API gateway?", "Single entry point routing requests to services", "A CSS preprocessing compilation tool", "A database query optimization layer", "A frontend page routing library", "A"),
                ("What is server-side rendering (SSR)?", "Generating full HTML on the server per request", "Styling CSS files on the server", "Caching JS bundles on the server only", "Running browser JavaScript on the server", "A"),
                ("What is client-side rendering (CSR)?", "Browser renders the UI using JS after page load", "Server sends fully rendered HTML pages", "CSS styles rendered by a remote CDN", "Database engine renders HTML templates", "A"),
                ("What is a headless CMS?", "CMS delivering content via API without a frontend", "A CMS system with no admin interface", "A database schema without any tables", "A framework with only a frontend layer", "A"),
                ("What is GraphQL?", "Query language letting clients request exact data", "A graph-based NoSQL database engine", "A CSS grid layout framework", "A unit and integration testing library", "A"),
                ("What is a message queue used for?", "Async communication buffer between services", "A database storage table variant", "A frontend client-side routing system", "A centralized server logging mechanism", "A"),
                ("What is separation of concerns?", "Different code parts each handle distinct tasks", "Keeping the entire codebase in one file", "Merging frontend and backend into one layer", "Reusing the exact same function everywhere", "A"),
                # SET 2
                ("What is WebSocket?", "Full-duplex real-time bidirectional protocol", "A one-way request-response HTTP protocol", "A CSS keyframe animation event system", "A database change notification protocol", "A"),
                ("What is AJAX?", "Async HTTP requests without full page reloads", "A standalone JavaScript UI framework", "A CSS preprocessor and build tool", "A SQL database query language variant", "A"),
                ("What format do REST APIs commonly return?", "JSON-formatted structured data", "Full HTML page document content", "CSS stylesheet rule definitions", "Only raw binary file data streams", "A"),
                ("What is OAuth2?", "Standard authorization protocol via third parties", "A password hashing and salting algorithm", "A low-level database wire protocol", "A responsive CSS design framework", "A"),
                ("What is a webhook?", "HTTP callback triggered by a remote event", "A frontend UI animation callback hook", "A database row-level trigger function", "A CSS nth-child pseudo-selector", "A"),
                ("What is session management?", "Maintaining user state across multiple HTTP requests", "Managing CSS visual theme configurations", "Handling all database connection pooling", "Routing and directing frontend page requests", "A"),
                ("Token-based auth vs session-based auth?", "Token is stateless; session is stored server-side", "Token stored in DB; session stored in browser", "Both authentication methods are server-side", "Both token and session approaches are stateless", "A"),
                ("What is a reverse proxy?", "Server forwarding client requests to backend services", "A frontend browser-side caching layer only", "A database query plan optimizer tool", "A CSS style sheet compilation pipeline tool", "A"),
                ("What is CORS and why is it needed?", "Controls cross-origin browser HTTP requests securely", "A CSS layout box model specification", "A JavaScript ES module import system", "A database table schema language", "A"),
                ("What is a service health check endpoint?", "URL verifying a running service is healthy", "A database index integrity check utility", "A CSS media query breakpoint check", "A JavaScript syntax validation test function", "A"),
                # SET 3
                ("What is CI/CD?", "Automated pipeline for building, testing, deploying", "A popular CSS utility framework library", "A database schema versioning migration tool", "A client-side frontend routing solution", "A"),
                ("What is a Docker container?", "Isolated portable environment running one app", "A fully virtualized hardware machine", "A dedicated remote cloud server instance", "A distributed database storage cluster", "A"),
                ("What is end-to-end testing?", "Testing full user flow from UI through backend", "Testing only the database persistence layer", "Visually testing CSS styles across browsers", "Isolating and unit testing single components", "A"),
                ("What is a staging environment?", "Pre-production environment for final integration tests", "The live production server receiving real users", "A developer's local development machine", "A dedicated offsite database backup server", "A"),
                ("What is blue-green deployment?", "Two identical envs with instant traffic switching", "Deploying exclusively to blue-tagged servers", "A Docker multi-stage build container strategy", "A database point-in-time backup strategy", "A"),
                ("What is a deployment rollback?", "Reverting the system to a previous good release", "Creating a snapshot database backup copy", "Clearing all cached CSS stylesheet files", "Wiping and clearing the frontend build cache", "A"),
                ("What is infrastructure as code (IaC)?", "Defining and managing infrastructure via config files", "Writing SQL scripts for data migrations only", "Styling entire applications using CSS variables", "Creating database schemas through a GUI tool", "A"),
                ("What is a code linter?", "Tool detecting code errors and style violations", "A module bundler for JavaScript applications", "A CSS compilation and minification tool", "A database schema migration runner tool", "A"),
                ("What is unit testing?", "Testing individual isolated functions or methods", "Testing the entire application as one system", "Testing only the database schema definitions", "Testing all REST API endpoints in sequence", "A"),
                ("What is a feature flag?", "Toggle enabling a feature without redeployment", "A CSS animation control property flag", "A dedicated git feature development branch", "A nullable boolean database table column", "A"),
            ],
            'mobile': [
                # SET 1
                ("What is React Native?", "JS framework producing native mobile apps", "A mobile-specific CSS styling framework", "A native iOS-only development SDK", "An Android-exclusive UI framework", "A"),
                ("What is Flutter?", "Google's Dart-based cross-platform UI toolkit", "A React-based native mobile wrapper", "An iOS-only mobile development framework", "A cross-platform mobile database engine", "A"),
                ("What is an Android APK file?", "Android application installable package file", "An iOS application distribution bundle", "A React Native JavaScript component file", "A mobile local database storage format", "A"),
                ("What does cross-platform mobile mean?", "Single codebase running on iOS and Android", "Maintaining separate codebases per platform", "An app that only runs inside a web browser", "An app using exclusively native platform code", "A"),
                ("What is Expo used for in React Native?", "Toolchain that simplifies React Native development", "A cross-platform mobile database system", "An iOS-specific hardware access SDK", "A mobile-focused CSS styling library", "A"),
                ("What is an Android Activity?", "A single screen presenting a user interface", "A background-only data processing service", "A database record access wrapper class", "A shareable XML layout resource file", "A"),
                ("Native app vs hybrid app?", "Native uses platform APIs; hybrid uses web tech", "Both approaches use only web technologies", "Native uses JavaScript; hybrid uses Swift", "There is no meaningful practical difference", "A"),
                ("What is AsyncStorage in React Native?", "Persistent unencrypted key-value device storage", "Real-time data synchronization to the cloud", "A React Native UI layout display component", "A lightweight HTTP networking client library", "A"),
                ("What is an Android Fragment?", "Reusable UI portion embedded within an Activity", "A fully independent complete screen Activity", "A structured database record object type", "A CSS-equivalent layout styling definition", "A"),
                ("What is a mobile device emulator?", "Virtual device for testing apps without hardware", "A cloud-based tool to deploy apps to production", "A tool that generates the app installation bundle", "A tool to publish app builds to app stores", "A"),
                # SET 2
                ("What is React Navigation?", "Library for navigating between screens in RN", "A Redux-based state management solution", "A curated UI component library collection", "A React Native automated build tool", "A"),
                ("What is stack navigation in mobile?", "Screens pushed onto and popped off a stack", "A bottom tab bar navigation pattern", "A side drawer slide-out navigation menu", "A grid-based screen layout navigation", "A"),
                ("What is Redux Toolkit used for?", "Simplified centralized state management", "A React Native screen navigation library", "A lightweight mobile HTTP network client", "A mobile-specific UI animation library", "A"),
                ("What is Context API used for in React Native?", "Sharing global state without prop drilling", "Making HTTP network API requests", "Handling all screen routing navigation", "Building and composing reusable UI layouts", "A"),
                ("What is deep linking in mobile apps?", "Opening a specific screen directly via URL", "Connecting the application to a backend DB", "Linking multiple CSS stylesheets together", "Sharing a codebase between multiple apps", "A"),
                ("What is tab navigation in mobile?", "Switching views via a persistent bottom tab bar", "Swiping between screens with gesture input", "Infinite scroll-based content navigation", "Opening screens via push notification taps", "A"),
                ("What does useEffect do in React Native?", "Handles side effects like data fetching", "Defines component visual styles and themes", "Declares component-level state variables", "Configures navigation route parameters", "A"),
                ("What is the Zustand library?", "Lightweight global state management for React", "A screen-to-screen navigation routing library", "A mobile application UI testing framework", "A CSS-in-JS component styling solution", "A"),
                ("What is a drawer navigator?", "Side menu that slides in from the screen edge", "A screen stack push-and-pop navigation mode", "A horizontally scrollable bottom tab bar", "A full-screen modal overlay dialog navigator", "A"),
                ("What does FlatList do in React Native?", "Renders large scrollable lists with virtualization", "Renders a fixed two-column photo grid layout", "Displays full-screen modal dialog overlays", "Manages all input form field components", "A"),
                # SET 3
                ("What is Hermes in React Native?", "JS engine optimized for React Native startup", "A UI component styling library for RN", "A screen navigation package for RN apps", "A centralized global state management tool", "A"),
                ("What are mobile push notifications?", "Server-initiated messages delivered to devices", "In-app pop-up notification dialogs only", "Email alerts delivered via SMTP servers", "SMS text messages sent via mobile carrier", "A"),
                ("What is geolocation in mobile apps?", "Accessing the device GPS position coordinates", "Monitoring app render performance metrics", "Managing device local file storage access", "Processing and displaying push notifications", "A"),
                ("What is a splash screen in mobile apps?", "Initial branded screen displayed during app load", "The main dashboard screen after login", "The user account login or sign-in screen", "A full-screen in-app error display screen", "A"),
                ("What is mobile app code signing?", "Cryptographic signature verifying app authenticity", "A source code style compilation process", "A binary build compression and zip step", "A database schema versioning migration step", "A"),
                ("Debug build vs release build?", "Debug has logging; release is production-optimized", "There is no meaningful difference between them", "Debug builds execute significantly faster", "Release builds contain more developer features", "A"),
                ("What is offline-first mobile development?", "Designing app to fully function without internet", "Requiring a constant live internet connection", "A native-code-only iOS development approach", "A backend API architecture design pattern", "A"),
                ("What is a native module in React Native?", "Bridge that connects JavaScript to native APIs", "A purely JavaScript-only UI display component", "A React Navigation screen routing module", "A centralized Redux state management module", "A"),
                ("What is mobile app performance optimization?", "Reducing render time, memory usage, and battery", "Adding more visual transitions and animations", "Increasing the total number of app screens", "Using the highest resolution image assets", "A"),
                ("What is the purpose of code obfuscation?", "Protecting app logic from reverse engineering", "Making source code more human-readable", "Significantly speeding up the build process", "Minimizing the final app installation size", "A"),
            ],
            'android': [
                # SET 1
                ("What is the recommended language for Android?", "Kotlin", "Swift", "Dart", "Ruby", "A"),
                ("What is an Android Activity?", "A single screen the user interacts with", "A background-only data service", "A data repository layer class", "An XML layout resource file", "A"),
                ("What is AndroidManifest.xml?", "Config declaring app components and permissions", "The main application Kotlin source file", "A reusable XML layout resource file", "A SQL database schema definition file", "A"),
                ("What is a Fragment in Android?", "Reusable UI component inside an Activity", "A fully standalone complete screen", "A background processing thread class", "A runtime permission request object", "A"),
                ("What is RecyclerView used for?", "Efficiently displaying large scrollable lists", "Showing a single non-scrollable item", "Handling in-app screen navigation", "Displaying modal alert dialog boxes", "A"),
                ("What is an Android Intent?", "Messaging object starting activities or services", "A visual UI animation class definition", "A database query wrapper object", "A REST HTTP network request object", "A"),
                ("What is Android ViewModel?", "Holds UI data surviving configuration changes", "An XML layout template definition file", "A local database access manager class", "A REST API network request client", "A"),
                ("What is the Room library?", "Android SQLite abstraction layer by Google", "A Firebase real-time cloud database", "A MongoDB-compatible NoSQL database", "An HTTP response caching library", "A"),
                ("What is Kotlin null safety?", "Distinguishing nullable vs non-nullable types", "Auto-removing null values from collections", "Preventing all possible app runtime crashes", "Completely disabling all null value usage", "A"),
                ("What is a Kotlin data class?", "Class auto-generating equals, hashCode, copy, toString", "A class storing only integer values", "An abstract class with no properties", "A class serving as an interface only", "A"),
                # SET 2
                ("What is the MVVM pattern in Android?", "Model-View-ViewModel separating UI from logic", "Model-View-Manager architecture pattern", "Machine View Visualizer design pattern", "Multi Value Map caching system", "A"),
                ("What is LiveData in Android?", "Lifecycle-aware observable data holder", "A background task scheduling library", "A third-party networking HTTP library", "An XML layout inflater utility class", "A"),
                ("What is Hilt in Android development?", "Dependency injection framework for Android", "A UI keyframe animation library", "A database ORM and migration tool", "A REST API networking client library", "A"),
                ("What is Retrofit used for?", "Type-safe HTTP client library for Android", "A UI layout management library", "A database versioning migration tool", "A unit and integration test helper", "A"),
                ("What is Jetpack Compose?", "Declarative UI toolkit for Android by Google", "An XML-based layout inflation system", "A Node.js-based backend framework", "A local SQLite database library", "A"),
                ("What is the Repository pattern?", "Abstracts data sources from ViewModels", "A UI component design pattern", "A network request result caching strategy", "An XML layout file structural pattern", "A"),
                ("What is WorkManager used for?", "Scheduling guaranteed deferrable background tasks", "Managing all UI layout inflation processes", "Handling all application network requests", "Controlling all in-app UI animations", "A"),
                ("What is a Kotlin Coroutine?", "Lightweight primitive for async concurrent code", "An Android architectural design pattern", "A declarative layout file manager", "A database transaction wrapper utility", "A"),
                ("What is the Navigation Component?", "Jetpack library managing fragment navigation", "A UI color theme management system", "A Retrofit-based networking library wrapper", "A local Room database access helper", "A"),
                ("What is DataBinding in Android?", "Connects UI views to data directly in XML", "A database network sync protocol", "A background schema migration tool", "A runtime user permissions manager", "A"),
                # SET 3
                ("What does ProGuard/R8 do in Android?", "Shrinks and obfuscates the production APK", "Inspects layout hierarchy visually", "Creates encrypted database backup files", "Monitors live network request traffic", "A"),
                ("APK vs AAB difference?", "APK is complete; AAB lets Play Store optimize", "Both formats are completely identical", "AAB is used exclusively for iOS apps", "APK is used for Progressive Web Apps", "A"),
                ("What is Android's runtime permission model?", "Users grant or deny permissions at runtime", "Apps have all permissions by default always", "Permissions are only set during app install", "All permissions are permanently optional", "A"),
                ("What is Espresso in Android?", "UI testing framework for Android by Google", "A local database access library", "A REST networking HTTP client library", "A Gradle-based build automation tool", "A"),
                ("What is a BroadcastReceiver?", "Listens for system or app-wide broadcast events", "Manages direct database table access", "Handles incoming HTTP network responses", "Controls all in-app UI animations", "A"),
                ("What is Firebase Authentication?", "Ready-made auth solution for Android and web", "A real-time cloud-only database service", "A Firebase-based cloud storage service", "A crash reporting and analytics tool", "A"),
                ("What is a memory leak in Android?", "Object no longer needed held in memory", "A dropped network connection timeout", "A null pointer NullPointerException crash", "A visual layout rendering glitch artifact", "A"),
                ("What is the Android Keystore system?", "Secure storage for cryptographic keys on device", "A file system local storage directory", "A Room-managed SQLite database store", "A Retrofit network request interceptor", "A"),
                ("What is Gradle in Android development?", "Build automation tool managing dependencies", "A declarative Compose UI layout library", "A Jetpack-based UI component testing tool", "A Room-compatible database ORM library", "A"),
                ("What is an Android Service component?", "Component running operations in the background", "A component rendering the main UI screen", "A Kotlin data class for model objects", "A broadcast listener event handler", "A"),
            ],
            'devops': [
                # SET 1
                ("What is Docker primarily used for?", "Building and running isolated containers", "A cloud-hosted relational database", "A frontend JavaScript UI framework", "A CSS preprocessor build tool", "A"),
                ("What is a Docker image?", "Read-only template used to create containers", "A currently running container instance", "A shell script of Docker commands", "A virtual machine disk snapshot", "A"),
                ("What is a Dockerfile?", "Script with instructions to build a Docker image", "A Docker container runtime log file", "A virtual container network config", "A Docker-managed SQL database file", "A"),
                ("What is docker-compose used for?", "Running and linking multi-container applications", "Building a single Docker image only", "Monitoring running container health", "Providing cloud-hosted Docker services", "A"),
                ("What is a container registry?", "Storage service for Docker images like Docker Hub", "A container runtime log database", "A container virtual network switch", "A container performance log store", "A"),
                ("What does 'docker run' do?", "Creates and starts a new container instance", "Builds a new Docker image from source", "Pushes a local image to a registry", "Stops and removes a running container", "A"),
                ("Image vs container in Docker?", "Image is a template; container is running instance", "Both an image and container are identical", "Container is read-only; image is running", "There is no practical difference here", "A"),
                ("What is container orchestration?", "Managing deployment and scaling of containers", "Writing and building all Dockerfile scripts", "Compiling and packaging container images", "Archiving and rotating container log files", "A"),
                ("What is Kubernetes?", "Container orchestration platform by Google", "A drop-in replacement alternative to Docker", "A Jenkins-based CI/CD pipeline tool", "A Prometheus-based monitoring platform", "A"),
                ("What is a Docker volume?", "Persistent storage mounted into containers", "A Docker container virtual network", "A read-only image filesystem layer", "A Docker daemon debug log file", "A"),
                # SET 2
                ("What is Continuous Integration (CI)?", "Auto building and testing code on every push", "Automatically deploying to production servers", "Monitoring production server health metrics", "Managing production database migrations", "A"),
                ("What is Continuous Deployment (CD)?", "Auto deploying passing builds to production", "Manually triggering all test suite runs", "Creating and rotating database backups", "Monitoring server performance dashboards", "A"),
                ("What is a CI/CD pipeline?", "Automated steps from commit to live deployment", "A Docker networking configuration file", "A Kubernetes pod deployment manifest", "A Terraform infrastructure provisioning file", "A"),
                ("What tool is GitHub Actions used for?", "Automating CI/CD workflows in GitHub repos", "Hosting and reviewing pull request diffs", "Managing GitHub repository access control", "Deploying static sites to GitHub Pages only", "A"),
                ("What is infrastructure as code (IaC)?", "Defining and versioning infra in config files", "Manually configuring servers via SSH sessions", "Writing shell scripts to install dependencies", "Creating cloud resources through a web GUI", "A"),
                ("What is Terraform used for?", "Provisioning cloud infrastructure via code", "Monitoring containerized app performance", "Running automated CI/CD pipeline jobs", "Managing Docker container registries", "A"),
                ("What is Ansible used for?", "Automating server configuration and provisioning", "Orchestrating Kubernetes pod deployments", "Building and pushing Docker container images", "Monitoring distributed system log streams", "A"),
                ("What is a Helm chart?", "Kubernetes app package and deployment template", "A Grafana dashboard chart configuration", "A Prometheus alerting rule definition", "A Terraform variable declaration file", "A"),
                ("What is a CI artifact?", "Build output stored for use in later pipeline steps", "A Kubernetes persistent volume claim", "A Docker image stored in a registry", "A Terraform state file snapshot backup", "A"),
                ("What is GitOps?", "Managing infra and deployments via Git workflows", "A GitHub feature for managing open-source forks", "A Jenkins plugin for managing pipelines", "A Docker Compose multi-environment tool", "A"),
                # SET 3
                ("What is Prometheus used for?", "Collecting and querying metrics from services", "Visualizing dashboards for collected metrics", "Centralizing and aggregating application logs", "Managing Docker container image storage", "A"),
                ("What is Grafana used for?", "Visualizing metrics data in dashboards", "Collecting raw metrics from all services", "Deploying Kubernetes application workloads", "Running CI/CD pipeline automation jobs", "A"),
                ("What is a Kubernetes Pod?", "Smallest deployable unit running one or more containers", "A standalone Docker container process", "A Kubernetes cluster node machine", "A Helm chart deployment configuration", "A"),
                ("What is auto-scaling in cloud infra?", "Dynamically adjusting resources based on demand", "Manually provisioning extra servers on request", "Scheduled nightly server restart processes", "Backing up data based on load thresholds", "A"),
                ("What is a rolling deployment?", "Gradually replacing old instances with new ones", "Instantly replacing all instances at once", "Deploying only to a single server at a time", "Routing all traffic to a staging environment", "A"),
                ("What is a load balancer?", "Distributes incoming traffic across server instances", "Monitors server logs for anomalies", "Creates and manages database backups", "Encrypts all inbound network connections", "A"),
                ("What is secrets management in DevOps?", "Securely storing and accessing credentials", "Committing secrets to a private git repo", "Hardcoding secrets in environment code", "Sharing secrets via an encrypted email", "A"),
                ("What is observability in DevOps?", "Understanding system state via logs, metrics, traces", "Watching live container console outputs", "Running automated end-to-end test suites", "Auditing all git commit message history", "A"),
                ("What is a canary deployment?", "Rolling out changes to a small user subset first", "Deploying only to canary cloud region servers", "Running tests only in the staging environment", "Instantly switching all traffic to new version", "A"),
                ("What is SLA in DevOps?", "Agreed uptime and performance service commitment", "A Kubernetes deployment YAML manifest file", "A Terraform module output variable block", "A Prometheus alerting notification rule", "A"),
            ],
            'data_science': [
                # SET 1
                ("What is a Pandas DataFrame?", "2D labeled table structure for data in Python", "A graph visualization library", "A deep learning model type", "A Python web scraping tool", "A"),
                ("What does NumPy provide for Python?", "Efficient N-dimensional array operations", "GUI building tools for Python", "Web request handling utilities", "Database ORM for Python apps", "A"),
                ("What is data cleaning?", "Fixing missing, incorrect, or inconsistent data", "Removing all data from a dataset", "Sorting data in ascending order", "Converting data to JSON format", "A"),
                ("What is exploratory data analysis (EDA)?", "Summarizing datasets to find patterns and insights", "Training machine learning models on data", "Deploying models to a production server", "Writing SQL queries against a database", "A"),
                ("What is a missing value in a dataset?", "An absent or null entry for a feature", "A duplicate row in the data", "An outlier value far from the mean", "A column with all zero values", "A"),
                ("What is feature engineering?", "Creating or transforming features to improve models", "Selecting the best ML algorithm to use", "Cleaning raw data before processing", "Deploying a trained ML model", "A"),
                ("What is data normalization?", "Scaling numeric features to a standard range", "Removing all null values from data", "Splitting data into train and test sets", "Encoding categorical variables", "A"),
                ("What is a train/test split?", "Dividing data into training and evaluation sets", "Removing duplicates from a dataset", "Normalizing all numeric feature values", "Visualizing data with matplotlib charts", "A"),
                ("What is a correlation matrix?", "Table showing pairwise feature correlations", "A confusion matrix for classifiers", "A list of model hyperparameters", "A chart showing model accuracy over time", "A"),
                ("What is matplotlib used for?", "Creating static data visualizations in Python", "Training neural network models", "Handling HTTP API requests in Python", "Managing SQL database connections", "A"),
                # SET 2
                ("What is supervised learning?", "Training on labeled input-output example pairs", "Training without any labeled data", "Clustering unlabeled data into groups", "Reducing the number of data features", "A"),
                ("What is unsupervised learning?", "Finding patterns in data without labels", "Training on labeled output data pairs", "Classifying images using CNN models", "Predicting continuous numeric values", "A"),
                ("What is a classification problem?", "Predicting a discrete category label for input", "Predicting a continuous numeric output value", "Grouping similar data points into clusters", "Reducing data to fewer dimensions", "A"),
                ("What is a regression problem?", "Predicting a continuous numeric output value", "Predicting a discrete category for input", "Detecting anomalies in a data stream", "Translating text from one language to another", "A"),
                ("What is overfitting in ML?", "Model performs well on train but poorly on test", "Model performs well on both train and test", "Model fails to learn from training data", "Model trains too slowly on large datasets", "A"),
                ("What is cross-validation?", "Evaluating model by rotating train/test splits", "Training the model multiple times in parallel", "Using multiple models and averaging outputs", "Applying regularization to reduce overfitting", "A"),
                ("What is a confusion matrix?", "Table showing true vs predicted classification results", "A matrix of feature correlation values", "A heatmap of model training loss values", "A table listing all model hyperparameters", "A"),
                ("What is precision in classification?", "Ratio of true positives to all predicted positives", "Ratio of true positives to all actual positives", "Accuracy of the model on the training set", "Number of correct predictions over all samples", "A"),
                ("What is recall in ML evaluation?", "Ratio of true positives to all actual positives", "Ratio of true positives to all predicted positives", "The harmonic mean of precision and recall", "Model accuracy on the held-out test set", "A"),
                ("What is a decision tree?", "Tree-based model splitting data by feature rules", "A neural network with multiple hidden layers", "A linear model for regression problems", "A clustering algorithm for unlabeled data", "A"),
                # SET 3
                ("What is a neural network?", "Computing model inspired by biological neurons", "A decision tree with many leaf nodes", "A linear regression with regularization", "A K-means clustering algorithm variant", "A"),
                ("What is deep learning?", "ML using neural networks with many hidden layers", "ML using only linear regression models", "ML relying solely on decision tree ensembles", "ML using K-nearest neighbor algorithms only", "A"),
                ("What is TensorFlow?", "Open-source ML framework by Google", "A Python data manipulation library", "A JavaScript visualization library", "A cloud database by Amazon", "A"),
                ("What is PyTorch?", "Open-source ML framework by Meta/Facebook", "A data processing library by Google", "A model deployment tool by Microsoft", "A database ORM for Python developers", "A"),
                ("What is a convolutional neural network (CNN)?", "Neural network specialized for image data", "Network specialized for sequential text data", "Network for tabular structured data only", "Network for reinforcement learning tasks", "A"),
                ("What is a recurrent neural network (RNN)?", "Neural network for sequential and time-series data", "Network specialized for image classification", "Network for tabular regression problems", "Network for unsupervised clustering tasks", "A"),
                ("What is transfer learning?", "Reusing a pretrained model for a new related task", "Training a model entirely from random weights", "Transferring data between two databases", "Moving a trained model to a new server", "A"),
                ("What is hyperparameter tuning?", "Optimizing model config values like learning rate", "Training the model on more data samples", "Adding more layers to a neural network", "Removing features from the training dataset", "A"),
                ("What is model deployment?", "Making a trained model available for predictions", "Training a model on a new dataset version", "Visualizing model evaluation metric charts", "Cleaning and preprocessing raw input data", "A"),
                ("What is a data pipeline?", "Automated flow processing data from source to output", "A neural network architecture pattern type", "A type of database indexing strategy", "A Python library for creating HTTP APIs", "A"),
            ],
            'ui_ux': [
                # SET 1
                ("What is UX design?", "Designing products focused on user experience", "Designing only the visual aesthetics of an app", "Writing backend code for web applications", "Creating database schemas for applications", "A"),
                ("What is UI design?", "Designing the visual interface users interact with", "Planning the overall product user journey", "Conducting user research and usability tests", "Writing frontend JavaScript component code", "A"),
                ("What is a wireframe?", "Low-fidelity layout sketch of a screen", "A high-fidelity interactive prototype", "A final polished production design file", "A CSS stylesheet for a web page", "A"),
                ("What is a prototype in UX?", "Interactive simulation of the final product", "A static image mockup of the design", "A written specification of features", "A coded production-ready web page", "A"),
                ("What is a design system?", "Reusable component library with design standards", "A CSS file containing all page styles", "A Figma file with all screen designs", "A brand logo and color palette only", "A"),
                ("What is information architecture (IA)?", "Organizing and structuring content for findability", "Designing the visual hierarchy of a screen", "Writing copy and microcopy for a product", "Coding the navigation menu of a website", "A"),
                ("What is a user persona?", "Fictional user representing a target audience group", "A real user who tests the product", "A heatmap of user click behavior", "A list of all app features and use cases", "A"),
                ("What is visual hierarchy?", "Arranging elements by importance to guide attention", "Equal sizing of all visual design elements", "Randomizing font sizes for visual variety", "Making all text the same color and weight", "A"),
                ("What is accessibility (a11y) in design?", "Designing products usable by people with disabilities", "Making a website load as fast as possible", "Ensuring the website works on all browsers", "Optimizing images and assets for web", "A"),
                ("What is the Gestalt principle of proximity?", "Items placed close together are perceived as related", "Similar-looking items are grouped together", "The eye follows a directional path naturally", "Objects are seen as whole rather than parts", "A"),
                # SET 2
                ("What is usability testing?", "Observing real users completing tasks on a product", "Automated testing of frontend components", "A/B testing two marketing campaign versions", "Measuring page load performance metrics", "A"),
                ("What is an A/B test in UX?", "Comparing two design variations with real users", "Testing a design across two different browsers", "Testing a mobile and desktop version", "Comparing two backend API implementations", "A"),
                ("What is a user flow?", "Path a user takes to complete a specific task", "A chart showing all app database queries", "A list of all pages in the application", "A diagram of all backend API endpoints", "A"),
                ("What is a heuristic evaluation?", "Expert review of UI against usability principles", "User testing sessions with real participants", "Automated accessibility auditing tool scan", "Performance profiling of a web application", "A"),
                ("What is Fitts's Law in UX?", "Larger and closer targets are faster to click", "Users read content left to right always", "Simpler designs are always more usable", "Users always notice top-of-page content first", "A"),
                ("What is color contrast in accessibility?", "Sufficient difference between text and background color", "Using many bright colors on a single screen", "Applying only one color throughout an interface", "Matching background and foreground colors exactly", "A"),
                ("What is the purpose of a style guide?", "Documenting consistent design rules for a product", "A list of all features for the product backlog", "A technical spec for backend API development", "A user research report with test findings", "A"),
                ("What is micro-interaction in UX?", "Small animations providing feedback to user actions", "Major redesigns of core product flows", "Backend API response handling logic", "Database query result display formatting", "A"),
                ("What is responsive design?", "Layouts adapting to different screen sizes", "Designing only for desktop screen sizes", "Creating separate apps for each device type", "Using fixed pixel widths for all elements", "A"),
                ("What is card sorting in UX research?", "Users grouping content to reveal mental models", "Sorting user feedback by sentiment score", "Ranking design mockups by visual appeal", "Ordering features by development priority", "A"),
                # SET 3
                ("What is Figma primarily used for?", "Collaborative UI/UX design and prototyping", "Writing and deploying frontend CSS code", "Managing design team project backlogs", "Creating marketing content and graphics", "A"),
                ("What is atomic design?", "Building UI from atoms up to full page templates", "Designing only the smallest UI components", "A physics-based UI animation framework", "A CSS architecture naming methodology", "A"),
                ("What is cognitive load in UX?", "Mental effort required to use a product", "Server processing time for API responses", "Number of screens in an application", "Amount of data stored in local storage", "A"),
                ("What is an affordance in UX design?", "A design cue that suggests how to interact with it", "A hidden feature only power users discover", "A system notification sent to the user", "A backend feature accessible via API", "A"),
                ("What is a pain point in UX?", "A frustration or obstacle in the user experience", "A slow-performing database query", "A bug in the frontend JavaScript code", "A missing feature requested by a stakeholder", "A"),
                ("What is the difference between UX and UI?", "UX is experience strategy; UI is visual execution", "UX is visual design; UI is backend logic", "UX and UI are exactly the same discipline", "UX is mobile-only; UI is desktop-only", "A"),
                ("What is a call-to-action (CTA)?", "A design element prompting a specific user action", "A backend API endpoint URL definition", "A marketing email campaign subject line", "A database stored procedure function", "A"),
                ("What is progressive disclosure in UX?", "Showing only necessary info to reduce overwhelm", "Displaying all features prominently at once", "Loading page content progressively on scroll", "Revealing hidden admin features to all users", "A"),
                ("What is an empathy map?", "Tool visualizing user thoughts, feelings, and actions", "A heatmap of user click behavior on screens", "A chart mapping features to user stories", "A table comparing competing product designs", "A"),
                ("What is design thinking?", "Human-centered problem-solving process with iteration", "A CSS methodology for component design", "A project management framework for designers", "A tool for generating design system tokens", "A"),
            ],
        }

        self._seed_questions(SECTOR_QUESTIONS)
        self.stdout.write(self.style.SUCCESS(
            'All 8 sectors seeded: frontend, backend, fullstack, mobile, android, devops, data_science, ui_ux'
        ))

    def _seed_questions(self, sector_questions):
        skills = Skill.objects.all()
        if not skills.exists():
            self.stdout.write(self.style.WARNING('No skills found. Run seed_skills first.'))
            return

        created = 0
        updated = 0

        import random

        with transaction.atomic():
            for skill in skills:
                sector = skill.category
                if sector not in sector_questions:
                    continue

                questions = sector_questions[sector]
                set_size = 10
                for idx, (q_text, opt_a, opt_b, opt_c, opt_d, orig_correct_opt) in enumerate(questions):
                    set_num = (idx // set_size) + 1
                    q_order = (idx % set_size) + 1
                    
                    # Deterministic shuffle
                    random.seed(q_text + str(idx))
                    
                    orig_options = [opt_a, opt_b, opt_c, opt_d]
                    opt_map_orig = {'A': 0, 'B': 1, 'C': 2, 'D': 3}
                    correct_text = orig_options[opt_map_orig.get(orig_correct_opt, 0)]

                    shuffled_options = orig_options.copy()
                    random.shuffle(shuffled_options)

                    new_correct_idx = shuffled_options.index(correct_text)
                    new_correct_option = ['A', 'B', 'C', 'D'][new_correct_idx]

                    s_opt_a, s_opt_b, s_opt_c, s_opt_d = shuffled_options

                    obj, was_created = Question.objects.update_or_create(
                        skill=skill,
                        set_number=set_num,
                        question_order=q_order,
                        defaults={
                            'sector': sector,
                            'question_text': q_text,
                            'option_a': s_opt_a,
                            'option_b': s_opt_b,
                            'option_c': s_opt_c,
                            'option_d': s_opt_d,
                            'correct_option': new_correct_option,
                            'is_active': True,
                        }
                    )
                    if was_created:
                        created += 1
                    else:
                        updated += 1

                self.stdout.write(self.style.SUCCESS(
                    f"  Skill '{skill.skill_name}': {len(questions)} questions seeded."
                ))

        self.stdout.write(self.style.SUCCESS(
            f'Done. Created: {created}, Updated: {updated}.'
        ))
