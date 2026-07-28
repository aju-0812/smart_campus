import { Card, CardContent, CardHeader, CardTitle } from "../components/ui/card";
import { FileText } from "lucide-react";
export default function ExamsPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Exam Agent</h1>
        <p className="text-muted-foreground mt-1">Automated scheduling and result analysis.</p>
      </div>
      <Card>
        <CardHeader><CardTitle className="flex items-center gap-2"><FileText className="h-5 w-5" /> Exam Schedule</CardTitle></CardHeader>
        <CardContent><p className="text-muted-foreground">Exams module integrated.</p></CardContent>
      </Card>
    </div>
  );
}
