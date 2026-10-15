import copy
import io
import unittest
from redact import redact,process
class Tests(unittest.TestCase):
    def test_nested_fields(self): self.assertEqual(redact({'a':[{'token':'demo'}]}),{'a':[{'token':'[REDACTED]'}]})
    def test_case_insensitive(self): self.assertEqual(redact({'PASSWORD':'demo'})['PASSWORD'],'[REDACTED]')
    def test_custom_field(self): self.assertEqual(redact({'ssn':'fake'},{'ssn'})['ssn'],'[REDACTED]')
    def test_preserve_values(self): self.assertEqual(redact({'latency':5,'ok':True,'empty':None}),{'latency':5,'ok':True,'empty':None})
    def test_no_mutation(self):
        v={'token':'demo'};b=copy.deepcopy(v);redact(v);self.assertEqual(v,b)
    def test_bad_line_never_echoed(self):
        with self.assertRaises(ValueError) as caught: process(io.StringIO('private malformed content'),io.StringIO())
        self.assertNotIn('private',str(caught.exception))
    def test_stream(self):
        out=io.StringIO();self.assertEqual(process(io.StringIO('\n{"token":"demo"}\n'),out),1);self.assertNotIn('demo',out.getvalue())
    def test_free_text_is_outside_scope(self): self.assertEqual(redact({'message':'token=demo'})['message'],'token=demo')
if __name__=='__main__': unittest.main()
