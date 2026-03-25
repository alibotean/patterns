package behavioral.template_method;

/**
 * Template Method Pattern
 *
 * Intent: Define the skeleton of an algorithm in a base-class method, deferring
 * some steps to subclasses. Subclasses redefine certain steps without changing
 * the algorithm's overall structure.
 *
 * Use when: Several classes share the same overall process but differ in specific steps.
 * The pattern avoids duplicating the common scaffolding in every subclass.
 */

/**
 * Defines the template method (generateReport) and the fixed steps.
 * Variable steps are abstract — each subclass fills them in differently.
 */
abstract class ReportGenerator {

    /**
     * The template method — the algorithm skeleton.
     * Declared final so subclasses cannot reorder or skip steps.
     */
    public final void generateReport(String title) {
        openDocument(title);
        writeHeader(title);
        writeBody();       // abstract — varies by subclass
        writeFooter();     // abstract — varies by subclass
        closeDocument();
    }

    // ── Fixed steps (common to all report types) ─────────────────────────────

    private void openDocument(String title) {
        System.out.println("[open]    Starting document: \"" + title + "\"");
    }

    private void writeHeader(String title) {
        System.out.println("[header]  Title: " + title + "  |  Generated: 2026-03-25");
    }

    private void closeDocument() {
        System.out.println("[close]   Document finalised.\n");
    }

    // ── Variable steps (subclasses must implement) ────────────────────────────

    /** Write the main content of the report. */
    protected abstract void writeBody();

    /** Write the closing section of the report. */
    protected abstract void writeFooter();
}

// ── Concrete Report Types ─────────────────────────────────────────────────────

class SalesReport extends ReportGenerator {
    @Override
    protected void writeBody() {
        System.out.println("[body]    Revenue Q1: $1,200,000");
        System.out.println("[body]    Revenue Q2: $1,450,000");
        System.out.println("[body]    Top product: Widget Pro");
    }

    @Override
    protected void writeFooter() {
        System.out.println("[footer]  Prepared by: Sales Dept  |  Confidential");
    }
}

class HrReport extends ReportGenerator {
    @Override
    protected void writeBody() {
        System.out.println("[body]    Headcount: 342");
        System.out.println("[body]    New hires this quarter: 27");
        System.out.println("[body]    Attrition rate: 4.2%");
    }

    @Override
    protected void writeFooter() {
        System.out.println("[footer]  Prepared by: HR Dept  |  Internal use only");
    }
}

// ── Demo ─────────────────────────────────────────────────────────────────────

public class Main {
    public static void main(String[] args) {
        // Same algorithm skeleton, different body and footer behaviour
        ReportGenerator sales = new SalesReport();
        sales.generateReport("Q2 Sales Summary");

        ReportGenerator hr = new HrReport();
        hr.generateReport("Q2 HR Overview");
    }
}
